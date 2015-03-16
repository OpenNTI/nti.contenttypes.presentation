#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
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

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import is_ntiid_of_types

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
from .interfaces import INTIAssignmentRef
from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewGroup

from . import RELATED_WORK
from . import RELATED_WORK_REF

from . import DISCUSSION_REF

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
		if 'desc' in parsed:
			parsed[u'description'] = parsed.pop('desc')
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

@component.adapter(INTIDiscussion)
class _NTIDiscussionUpdater(_TargetNTIIDUpdater):
	
	_ext_iface_upper_bound = INTIDiscussion
	
	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)	
		ntiid = parsed.get('ntiid')
		if parsed.get('target') and ntiid == parsed.get('target'):
			nttype = get_type(ntiid)
			if ':' in nttype:
				nttype = DISCUSSION_REF + nttype[nttype.index(':'):]
			else:
				nttype = DISCUSSION_REF
			ntiid = make_ntiid(nttype=nttype, base=ntiid)
			parsed['ntiid'] = ntiid
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

def internalization_pre_hook(k, x):
	if k==ITEMS and isinstance(x, MutableSequence):
		for item in x:
			if not isinstance(item, Mapping):
				continue
			mimeType = item.get(MIMETYPE)
			if mimeType == "application/vnd.nextthought.assessment.assignment": 
				item[MIMETYPE] = u"application/vnd.nextthought.assignmentref"
			elif mimeType == "application/vnd.nextthought.ntivideo":
				item[MIMETYPE] = u"application/vnd.nextthought.ntivideoref"
			elif mimeType == "application/vnd.nextthought.ntiaudio":
				item[MIMETYPE] = u"application/vnd.nextthought.ntiaudioref"
			elif mimeType == "application/vnd.nextthought.discussion":
				item[MIMETYPE] = u"application/vnd.nextthought.discussionref"
				
	elif isinstance(x, Mapping):
		mimeType = x.get(MIMETYPE)
		ntiid = x.get('ntiid') or x.get(NTIID)
		if 	not mimeType and ntiid and \
			is_ntiid_of_types(ntiid, (RELATED_WORK, RELATED_WORK_REF)):
			x[MIMETYPE] = "application/vnd.nextthought.relatedworkref"

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
