#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
import copy
from collections import Mapping
from collections import MutableSequence

from zope import interface
from zope import component

from persistent.list import PersistentList

from nti.common.string import map_string_adjuster

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.interfaces import IInternalObjectUpdater
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.ntiids.ntiids import is_ntiid_of_type
from nti.ntiids.ntiids import is_ntiid_of_types

from .discussion import make_discussionref_ntiid

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTISlide
from .interfaces import INTIAudioRef
from .interfaces import INTITimeline
from .interfaces import INTIVideoRef
from .interfaces import INTISlideDeck
from .interfaces import INTIDiscussion
from .interfaces import INTISlideVideo
from .interfaces import INTIRelatedWork
from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIDiscussionRef
from .interfaces import INTIQuestionSetRef
from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewGroup

from . import TIMELINE
from . import JSON_TIMELINE

from . import RELATED_WORK
from . import RELATED_WORK_REF

ITEMS = StandardExternalFields.ITEMS
NTIID = StandardExternalFields.NTIID
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@interface.implementer(IInternalObjectUpdater)
class _NTIMediaUpdater(InterfaceObjectIO):

	def fixCreator(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')
		return self
	
	def parseTranscripts(self, parsed):
		transcripts = parsed.get('transcripts')
		for idx, transcript in enumerate(transcripts or ()):
			if MIMETYPE not in transcript:
				transcript[MIMETYPE] = u'application/vnd.nextthought.ntitranscript'
			obj = find_factory_for(transcript)()
			transcripts[idx] = update_from_external_object(obj, transcript)
		return self
		
	def fixAll(self, parsed):
		self.fixCreator(parsed).parseTranscripts(parsed)
		return parsed
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIMediaUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIVideo)
class _NTIVideoUpdater(_NTIMediaUpdater):

	_ext_iface_upper_bound = INTIVideo

	def parseSources(self, parsed):
		sources = parsed.get('sources')
		for idx, source in enumerate(sources or ()):
			if MIMETYPE not in source:
				source[MIMETYPE] = u'application/vnd.nextthought.ntivideosource'
			obj = find_factory_for(source)()
			sources[idx] = update_from_external_object(obj, source)
		return self

	def fixCloseCaption(self, parsed):
		if 'closedCaptions' in parsed:
			parsed[u'closed_caption'] = parsed['closedCaptions']
		elif 'closedCaption' in parsed:
			parsed[u'closed_caption'] = parsed['closedCaption']
		return self
	
	def fixAll(self, parsed):
		self.parseSources(parsed).parseTranscripts(parsed).fixCloseCaption(parsed).fixCreator(parsed)
		return parsed

@component.adapter(INTIAudio)
class _NTIAudioUpdater(_NTIMediaUpdater):

	_ext_iface_upper_bound = INTIAudio

	def parseSources(self, parsed):
		sources = parsed.get('sources')
		for idx, source in enumerate(sources or ()):
			if MIMETYPE not in source:
				source[MIMETYPE] = u'application/vnd.nextthought.ntiaudiosource'
			obj = find_factory_for(source)()
			sources[idx] = update_from_external_object(obj, source)
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed).parseSources(parsed).parseTranscripts(parsed)
		return parsed

@interface.implementer(IInternalObjectUpdater)
class _NTIMediaRefUpdater(InterfaceObjectIO):
		
	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = parsed.pop(NTIID)
		return parsed
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIMediaRefUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result
	
@interface.implementer(IInternalObjectUpdater)
class _NTIVideoRefUpdater(_NTIMediaRefUpdater):
	_ext_iface_upper_bound = INTIVideoRef

@interface.implementer(IInternalObjectUpdater)
class _NTIAudioRefUpdater(_NTIMediaRefUpdater):
	_ext_iface_upper_bound = INTIAudioRef	

@component.adapter(INTISlide)
@interface.implementer(IInternalObjectUpdater)
class _NTISlideUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTISlide
	
	def fixAll(self, parsed):
		for name, func in ( ("slidevideostart", float),
							("slidevideoend", float),
							("slidenumber", int)):
			
			value = parsed.get(name, None)
			if value is not None and isinstance(value, six.string_types):
				try:
					parsed[name] = func(value) 
				except (TypeError, ValueError):
					pass
		return self
		
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTISlideUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTISlideVideo)
@interface.implementer(IInternalObjectUpdater)
class _NTISlideVideoUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTISlideVideo
	
	def fixAll(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')
		
		if 'video-ntiid' in parsed:
			parsed[u'video_ntiid'] = parsed.pop('video-ntiid')

		return self
		
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTISlideVideoUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTISlideDeck)
@interface.implementer(IInternalObjectUpdater)
class _NTISlideDeckUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTISlideDeck
	
	def fixAll(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')

		if 'slidedeckid' in parsed and not parsed.get('ntiid'):
			parsed[u'ntiid'] = parsed['slidedeckid']

		if 'ntiid' in parsed and not parsed.get('slidedeckid'):
			parsed[u'slidedeckid'] = parsed['ntiid']

		return self
		
	def parseSlides(self, parsed):
		slides = PersistentList(parsed.get('Slides') or ())
		if slides:
			parsed[u'Slides'] = slides
		return self

	def parseVideos(self, parsed):
		videos = PersistentList(parsed.get('Videos') or ())
		if videos:
			parsed[u'Videos'] = videos
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		map_string_adjuster(parsed, recur=False)
		self.fixAll(parsed).parseSlides(parsed).parseVideos(parsed)
		result = super(_NTISlideDeckUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTITimeline)
@interface.implementer(IInternalObjectUpdater)
class _NTITimelineUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTITimeline
	
	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = parsed[NTIID]
		if 'desc' in parsed:
			parsed[u'description'] = parsed.pop('desc')
		if 'suggested-inline' in parsed:
			parsed[u'suggested_inline'] = parsed.pop('suggested-inline')
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTITimelineUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@interface.implementer(IInternalObjectUpdater)
class _TargetNTIIDUpdater(InterfaceObjectIO):
	
	def fixTarget(self, parsed, transfer=True):
		if NTIID in parsed:
			parsed[u'ntiid'] = parsed[NTIID]
		
		for name in ('Target-NTIID', 'target-NTIID', 'target-ntiid'):
			if name in parsed:
				parsed['target'] = parsed.pop(name)
				break

		if transfer:
			if not parsed.get('target') and parsed.get('ntiid'):
				parsed[u'target'] = parsed['ntiid']
			elif not parsed.get('ntiid') and parsed.get('target'):
				parsed[u'ntiid'] = parsed['target']

		return self

@component.adapter(INTIRelatedWork)
class _NTIRelatedWorkUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIRelatedWork
	
	def fixAll(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')
			
		if 'desc' in parsed:
			parsed[u'description'] = parsed.pop('desc')
		
		self.fixTarget(parsed, transfer=False)	
		
		if 'targetMimeType' in parsed:
			parsed[u'type'] = parsed.pop('targetMimeType')
			
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIRelatedWorkUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result
_NTIRelatedWorkRefUpdater = _NTIRelatedWorkUpdater

@component.adapter(INTIDiscussionRef)
class _NTIDiscussionRefUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIDiscussionRef
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)	
		ntiid = parsed.get('ntiid')
		if parsed.get('target') and ntiid == parsed.get('target'):
			ntiid = make_discussionref_ntiid(ntiid)
			parsed['ntiid'] = ntiid
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIDiscussionRefUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIDiscussion)
class _NTIDiscussionUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIDiscussion
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIDiscussionUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIAssignmentRef)
class _NTIAssignmentRefUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIAssignmentRef
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		if not parsed.get('title') and parsed.get('label'):
			parsed[u'title'] = parsed['label']
		elif not parsed.get('label') and parsed.get('title'):
			parsed[u'label'] = parsed['title']
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIAssignmentRefUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIQuestionSetRef)
class _NTIQuestionSetRefUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIQuestionSetRef
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		if 'question-count' in parsed:
			parsed[u'question_count'] = int(parsed.pop('question-count'))	
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIQuestionSetRefUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		return result
	
@component.adapter(INTIQuestionRef)
class _NTIQuestionRefUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIQuestionRef
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)			
		return self
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIQuestionRefUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTICourseOverviewGroup)
@interface.implementer(IInternalObjectUpdater)
class _NTICourseOverviewGroupUpdater(InterfaceObjectIO):

	_ext_iface_upper_bound = INTICourseOverviewGroup

	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = parsed[NTIID]
		items = PersistentList(parsed.get(ITEMS) or ())
		parsed[ITEMS] = items	
		return parsed
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed, recur=False))
		result = super(_NTICourseOverviewGroupUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTILessonOverview)
@interface.implementer(IInternalObjectUpdater)
class _NTILessonOverviewUpdater(InterfaceObjectIO):

	_ext_iface_upper_bound = INTILessonOverview

	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = parsed[NTIID]
		items = PersistentList(parsed.get(ITEMS) or ())
		parsed[ITEMS] = items	
		return parsed
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed, recur=False))
		result = super(_NTILessonOverviewUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

def internalization_ntivideo_pre_hook(k, x):
	if isinstance(x, Mapping) and 'mimeType' in x:
		x[MIMETYPE] = x.pop('mimeType')
internalization_ntiaudio_pre_hook = internalization_ntivideo_pre_hook

def internalization_assignmentref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.assessment.assignment": 
		x[MIMETYPE] = u"application/vnd.nextthought.assignmentref"
	
def internalization_questionsetref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.naquestionset": 
		x[MIMETYPE] = u"application/vnd.nextthought.questionsetref"
	
def internalization_questionref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.naquestion": 
		x[MIMETYPE] = u"application/vnd.nextthought.questionref"
				
def internalization_ntivideoref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.ntivideo": 
		x[MIMETYPE] = u"application/vnd.nextthought.ntivideoref"
	
def internalization_ntiaudioref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.ntiaudio": 
		x[MIMETYPE] = u"application/vnd.nextthought.ntiaudioref"
	
def internalization_discussion_pre_hook(k, x):
	pass
		
def internalization_discussionref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.discussion": 
		x[MIMETYPE] = u"application/vnd.nextthought.discussionref"
	
def internalization_ntitimeline_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if not mimeType:
		ntiid = x.get('ntiid') or x.get(NTIID) if isinstance(x, Mapping) else None
		if ntiid and (JSON_TIMELINE in ntiid or is_ntiid_of_type(ntiid, TIMELINE)):
			x[MIMETYPE] = "application/vnd.nextthought.timeline"
	elif mimeType == "application/vnd.nextthought.ntitimeline": 
		x[MIMETYPE] = u"application/vnd.nextthought.timeline"
		
def internalization_relatedworkref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if not mimeType:
		ntiid = x.get('ntiid') or x.get(NTIID) if isinstance(x, Mapping) else None
		if 	ntiid and \
			(is_ntiid_of_types(ntiid, (RELATED_WORK, RELATED_WORK_REF)) or \
			 '.relatedworkref.' in ntiid): # old legacy courses
			x[MIMETYPE] = "application/vnd.nextthought.relatedworkref"
		
def internalization_courseoverview_pre_hook(k, x):
	if k==ITEMS and isinstance(x, MutableSequence):
		idx = 0
		while idx < len(x):
			item = x[idx]
			internalization_ntitimeline_pre_hook(None, item)
			internalization_ntiaudioref_pre_hook(None, item)
			internalization_ntivideoref_pre_hook(None, item)
			internalization_questionref_pre_hook(None, item)
			internalization_assignmentref_pre_hook(None, item)
			internalization_questionsetref_pre_hook(None, item)
			internalization_relatedworkref_pre_hook(None, item)
			
			mimeType = item.get(MIMETYPE) if isinstance(item, Mapping) else None
			if mimeType == "application/vnd.nextthought.discussion": 
				if 'body' in item or 'Body' in item: # fully model
					continue
				s = item.get(NTIID) or item.get('ntiid')
				ntiids = s.split(' ') if s else ()
				if len(ntiids) > 1:
					for c, ntiid in enumerate(ntiids):
						if c > 0:
							idx += 1
							item = copy.deepcopy(item)
							x.insert(idx, item)
						item[NTIID] = ntiid
						internalization_discussionref_pre_hook(None, item)
				elif not ntiids:# not yet ready
					del x[idx]
					continue
				else:
					internalization_discussionref_pre_hook(None, item)
			idx +=1

def internalization_lessonoverview_pre_hook(k, x):
	if k==ITEMS and isinstance(x, MutableSequence):
		for item in x:
			items = item.get(ITEMS) if isinstance(item, Mapping) else None
			if items is not None:
				internalization_courseoverview_pre_hook(ITEMS, items)
