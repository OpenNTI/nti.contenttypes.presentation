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

from zope import component
from zope import interface

from persistent.list import PersistentList

from nti.contenttypes.presentation import TIMELINE
from nti.contenttypes.presentation import RELATED_WORK
from nti.contenttypes.presentation import JSON_TIMELINE
from nti.contenttypes.presentation import RELATED_WORK_REF
from nti.contenttypes.presentation import TIMELINE_MIMETYES
from nti.contenttypes.presentation import NTI_LESSON_OVERVIEW
from nti.contenttypes.presentation import SLIDE_DECK_MIMETYES
from nti.contenttypes.presentation import TIMELINE_REF_MIMETYES
from nti.contenttypes.presentation import SLIDE_DECK_REF_MIMETYES
from nti.contenttypes.presentation import ALL_MEDIA_ROLL_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_MIMETYES
from nti.contenttypes.presentation import RELATED_WORK_REF_POINTER_MIMETYES

from nti.contenttypes.presentation.discussion import is_nti_course_bundle

from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTISlide
from nti.contenttypes.presentation.interfaces import INTIPollRef
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTISurveyRef
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import INTIQuestionRef
from nti.contenttypes.presentation.interfaces import INTITimelineRef
from nti.contenttypes.presentation.interfaces import INTISlideDeckRef
from nti.contenttypes.presentation.interfaces import INTIAssignmentRef
from nti.contenttypes.presentation.interfaces import INTIDiscussionRef
from nti.contenttypes.presentation.interfaces import INTIQuestionSetRef
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTICourseOverviewSpacer
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRefPointer

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.interfaces import IInternalObjectUpdater
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import is_ntiid_of_type
from nti.ntiids.ntiids import is_ntiid_of_types
from nti.ntiids.ntiids import is_valid_ntiid_string

ID = StandardExternalFields.ID
ITEMS = StandardExternalFields.ITEMS
NTIID = StandardExternalFields.NTIID
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

def ntiid_check(s):
	s = s.strip() if s else s
	s = s[1:] if s and (s.startswith('"') or s.startswith("'")) else s
	s = s[6:] if s and s.startswith("relwk:tag:") else s
	return s

@interface.implementer(IInternalObjectUpdater)
class _AssetUpdater(InterfaceObjectIO):

	def fixCreator(self, parsed):
		if 'creator' in parsed:
			parsed['byline'] = parsed.pop('creator')
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed)
		return parsed
	
	def takeOwnership(self, parent, items):
		for item in items or ():
			item.__parent__ = parent

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(parsed)
		result = super(_AssetUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

class _NTIMediaUpdater(_AssetUpdater):

	def parseTranscripts(self, parsed):
		transcripts = parsed.get('transcripts')
		for idx, transcript in enumerate(transcripts or ()):
			if not isinstance(transcript, Mapping):
				continue
			if MIMETYPE not in transcript:
				transcript[MIMETYPE] = u'application/vnd.nextthought.ntitranscript'
			obj = find_factory_for(transcript)()
			transcripts[idx] = update_from_external_object(obj, transcript)
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed).parseTranscripts(parsed)
		return parsed

@component.adapter(INTIVideo)
class _NTIVideoUpdater(_NTIMediaUpdater):

	_ext_iface_upper_bound = INTIVideo

	def parseSources(self, parsed):
		sources = parsed.get('sources')
		for idx, source in enumerate(sources or ()):
			if not isinstance(source, Mapping):
				continue
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
			if not isinstance(source, Mapping):
				continue
			if MIMETYPE not in source:
				source[MIMETYPE] = u'application/vnd.nextthought.ntiaudiosource'
			obj = find_factory_for(source)()
			sources[idx] = update_from_external_object(obj, source)
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed).parseSources(parsed).parseTranscripts(parsed)
		return parsed

class _TargetNTIIDUpdater(_AssetUpdater):

	TARGET_FIELDS = ('Target-NTIID', 'target-NTIID', 'target-ntiid', 'target')

	def popTargets(self, parsed):
		for name in self.TARGET_FIELDS:
			parsed.pop(name, None)
		return self

	def getTargetNTIID(self, parsed):
		for name in self.TARGET_FIELDS:
			if name in parsed:
				return ntiid_check(parsed.get(name))
		return None

	def fixTarget(self, parsed, transfer=True):
		if NTIID in parsed:
			parsed[u'ntiid'] = ntiid_check(parsed[NTIID])
		elif 'ntiid' in parsed:
			parsed[u'ntiid'] = ntiid_check(parsed[u'ntiid'])

		target = self.getTargetNTIID(parsed)
		if target:
			parsed['target'] = target

		if transfer:
			ntiid, target = parsed.get('ntiid'), parsed.get('target')
			if ntiid and not target:
				parsed['target'] = ntiid
				parsed.pop('ntiid', None)
				parsed.pop(NTIID, None)
		return self

class _NTIMediaRefUpdater(_TargetNTIIDUpdater):

	def fixTarget(self, parsed, transfer=False):
		return _TargetNTIIDUpdater.fixTarget(self, parsed, transfer=True)

	def fixAll(self, parsed):
		self.fixTarget(parsed).fixCreator(parsed)
		return parsed

class _NTIVideoRefUpdater(_NTIMediaRefUpdater):
	_ext_iface_upper_bound = INTIVideoRef

class _NTIAudioRefUpdater(_NTIMediaRefUpdater):
	_ext_iface_upper_bound = INTIAudioRef

@component.adapter(INTISlide)
class _NTISlideUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTISlide

	def fixAll(self, parsed):
		for name, func in (("slidevideostart", float),
						   ("slidevideoend", float),
						   ("slidenumber", int)):

			value = parsed.get(name, None)
			if value is not None and isinstance(value, six.string_types):
				try:
					parsed[name] = func(value)
				except (TypeError, ValueError):
					pass
		return self.fixCreator(parsed)

@component.adapter(INTISlideVideo)
class _NTISlideVideoUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTISlideVideo

	def fixAll(self, parsed):
		if 'video-ntiid' in parsed:
			parsed[u'video_ntiid'] = ntiid_check(parsed.pop('video-ntiid'))
		return self.fixCreator(parsed)

@component.adapter(INTISlideDeck)
class _NTISlideDeckUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTISlideDeck

	def parseSlides(self, parsed):
		if 'Slides' in parsed:
			slides = PersistentList(parsed.get('Slides') or ())
			parsed[u'Slides'] = slides
		return self

	def parseVideos(self, parsed):
		if 'Videos' in parsed:
			videos = PersistentList(parsed.get('Videos') or ())
			parsed[u'Videos'] = videos
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed)

		if 'slidedeckid' in parsed and not parsed.get('ntiid'):
			parsed[u'ntiid'] = ntiid_check(parsed['slidedeckid'])

		if 'ntiid' in parsed and not parsed.get('slidedeckid'):
			parsed[u'slidedeckid'] = ntiid_check(parsed['ntiid'])

		return self.parseSlides(parsed).parseVideos(parsed)

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		result = super(_NTISlideDeckUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		self.takeOwnership(self._ext_self, self._ext_self.Slides)
		self.takeOwnership(self._ext_self, self._ext_self.Videos)
		return result

@component.adapter(INTITimeline)
class _NTITimelineUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTITimeline

	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = ntiid_check(parsed[NTIID])
		if 'desc' in parsed:
			parsed[u'description'] = parsed.pop('desc')
		if 'suggested-inline' in parsed:
			parsed[u'suggested_inline'] = parsed.pop('suggested-inline')
		return self.fixCreator(parsed)

@component.adapter(INTIRelatedWorkRef)
class _NTIRelatedWorkRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIRelatedWorkRef

	def fixTarget(self, parsed, transfer=False):
		return _TargetNTIIDUpdater.fixTarget(self, parsed, transfer=False)

	def fixAll(self, parsed):
		if 'desc' in parsed:
			parsed[u'description'] = parsed.pop('desc')

		self.fixTarget(parsed)

		if 'targetMimeType' in parsed:
			parsed[u'type'] = parsed.pop('targetMimeType')

		return self.fixCreator(parsed)

_NTIRelatedWorkUpdater = _NTIRelatedWorkRefUpdater

@component.adapter(INTIDiscussionRef)
class _NTIDiscussionRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIDiscussionRef
	_excluded_in_ivars_ = InterfaceObjectIO._excluded_in_ivars_ - {'id'}

	def fixTarget(self, parsed, transfer=True):
		iden = parsed.get('id') or parsed.get(ID)
		if is_nti_course_bundle(iden):
			parsed['id'] = iden  # reset in case
			ntiid = ntiid_check(parsed.get(NTIID) or parsed.get('ntiid'))
			if not ntiid:
				parsed.pop(NTIID, None)

		# remove target fields if empty
		target = self.getTargetNTIID(parsed)
		if not target:
			self.popTargets(parsed)
		# complete
		return super(_NTIDiscussionRefUpdater, self).fixTarget(parsed, transfer=transfer)

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		ntiid = ntiid_check(parsed.get('ntiid'))
		if ntiid:
			parsed['ntiid'] = ntiid
		if not parsed.get('id') and ntiid:
			parsed['id'] = ntiid
		return self.fixCreator(parsed)

@component.adapter(INTIAssignmentRef)
class _NTIAssignmentRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIAssignmentRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		if not parsed.get('title') and parsed.get('label'):
			parsed[u'title'] = parsed['label']
		elif not parsed.get('label') and parsed.get('title'):
			parsed[u'label'] = parsed['title']
		return self.fixCreator(parsed)

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(parsed)
		result = super(_NTIAssignmentRefUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIQuestionSetRef)
class _NTIQuestionSetRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIQuestionSetRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		if 'question-count' in parsed:
			parsed[u'question_count'] = int(parsed.pop('question-count'))
		return self.fixCreator(parsed)

@component.adapter(INTIQuestionRef)
class _NTIQuestionRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIQuestionRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self.fixCreator(parsed)

@component.adapter(INTIPollRef)
class _NTIPollRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIPollRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self.fixCreator(parsed)

@component.adapter(INTISlideDeckRef)
class _NTISlideDeckRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTISlideDeckRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self.fixCreator(parsed)

@component.adapter(INTITimelineRef)
class _NTITimelineRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTITimelineRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self.fixCreator(parsed)

@component.adapter(INTIRelatedWorkRefPointer)
class _NTIRelatedWorkRefPointerUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTIRelatedWorkRefPointer

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		return self.fixCreator(parsed)

@component.adapter(INTISurveyRef)
class _NTISurveyRefUpdater(_TargetNTIIDUpdater):

	_ext_iface_upper_bound = INTISurveyRef

	def fixAll(self, parsed):
		self.fixTarget(parsed, transfer=True)
		if 'question-count' in parsed:
			parsed[u'question_count'] = int(parsed.pop('question-count'))
		return self.fixCreator(parsed)

@component.adapter(INTICourseOverviewSpacer)
class _NTICourseOverviewSpacerUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTICourseOverviewSpacer

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		result = super(_NTICourseOverviewSpacerUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		assert self._ext_replacement().ntiid, "No NTIID provided"
		return result

@component.adapter(INTIMediaRoll)
class _NTIMediaRollUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTIMediaRoll

	def fixAll(self, parsed):
		if ITEMS in parsed:
			items = PersistentList(parsed.get(ITEMS) or ())
			parsed[ITEMS] = items
		return super(_NTIMediaRollUpdater, self).fixAll(parsed)

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		result = super(_NTIMediaRollUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		self.takeOwnership(self._ext_self, self._ext_self)
		return result

@component.adapter(INTIAudioRoll)
class _NTIAudioRollUpdater(_NTIMediaRollUpdater):
	_ext_iface_upper_bound = INTIAudioRoll

@component.adapter(INTIVideoRoll)
class _NTIVideoRollUpdater(_NTIMediaRollUpdater):
	_ext_iface_upper_bound = INTIVideoRoll

@component.adapter(INTICourseOverviewGroup)
class _NTICourseOverviewGroupUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTICourseOverviewGroup

	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = ntiid_check(parsed[NTIID])
		# use persistent lists
		if ITEMS in parsed:
			items = PersistentList(parsed.get(ITEMS) or ())
			parsed[ITEMS] = items
		return self.fixCreator(parsed)

	def updateFromExternalObject(self, parsed, *args, **kwargs):
		result = super(_NTICourseOverviewGroupUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		self.takeOwnership(self._ext_self, self._ext_self)
		assert self._ext_self.ntiid, "No NTIID provided"
		return result

@component.adapter(INTILessonOverview)
class _NTILessonOverviewUpdater(_AssetUpdater):

	_ext_iface_upper_bound = INTILessonOverview

	def fixAll(self, parsed):
		if NTIID in parsed:
			parsed[u'ntiid'] = ntiid_check(parsed[NTIID])
		ntiid = parsed.get('ntiid')
		lesson = parsed.get('lesson')
		# make sure we update the incoming ntiid
		# since in legacy it may the ntiid of a content unit
		if 		not lesson \
			and is_valid_ntiid_string(ntiid) \
			and get_type(ntiid) != NTI_LESSON_OVERVIEW:
			lesson = make_ntiid(nttype=NTI_LESSON_OVERVIEW, base=ntiid)
			parsed[u'ntiid'] = lesson
			parsed[u'lesson'] = ntiid
		# use persistent lists
		if ITEMS in parsed:
			items = PersistentList(parsed.get(ITEMS) or ())
			parsed[ITEMS] = items
		return self.fixCreator(parsed)
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		result = super(_NTILessonOverviewUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
		self.takeOwnership(self._ext_self, self._ext_self)
		return result

def internalization_ntivideo_pre_hook(k, x):
	if isinstance(x, Mapping) and 'mimeType' in x:
		x[MIMETYPE] = x.pop('mimeType')
internalization_ntiaudio_pre_hook = internalization_ntivideo_pre_hook

def internalization_assignmentref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.assessment.assignment":
		x[MIMETYPE] = u"application/vnd.nextthought.assignmentref"

def internalization_surveyref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.nasurvey":
		x[MIMETYPE] = u"application/vnd.nextthought.surveyref"

def internalization_pollref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.napoll":
		x[MIMETYPE] = u"application/vnd.nextthought.pollref"

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

def internalization_discussionref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.discussion":
		x[MIMETYPE] = u"application/vnd.nextthought.discussionref"

def internalization_slidedeckref_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType in SLIDE_DECK_MIMETYES:
		x[MIMETYPE] = SLIDE_DECK_REF_MIMETYES[0]

def is_time_line(x):
	result = False
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if not mimeType:
		ntiid = x.get('ntiid') or x.get(NTIID) if isinstance(x, Mapping) else None
		if ntiid and (JSON_TIMELINE in ntiid or is_ntiid_of_type(ntiid, TIMELINE)):
			result = True
	elif mimeType in TIMELINE_MIMETYES:
		result = True
	return result
	
def internalization_ntitimeline_pre_hook(k, x):
	if is_time_line(x):
		x[MIMETYPE] = TIMELINE_MIMETYES[0]

def internalization_ntitimelineref_pre_hook(k, x):
	if is_time_line(x):
		x[MIMETYPE] = TIMELINE_REF_MIMETYES[0]

def is_relatedwork_ref(x):
	result = False
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if not mimeType:
		ntiid = x.get('ntiid') or x.get(NTIID) if isinstance(x, Mapping) else None
		if 		ntiid \
			and (	'.relatedworkref.' in ntiid
				 or is_ntiid_of_types(ntiid, (RELATED_WORK, RELATED_WORK_REF))):
			result = True
	elif mimeType in RELATED_WORK_REF_MIMETYES:
		result = True
	return result

def internalization_relatedworkref_pre_hook(k, x):
	if is_relatedwork_ref(x):
		x[MIMETYPE] = RELATED_WORK_REF_MIMETYES[0]

def internalization_relatedworkrefpointer_pre_hook(k, x):
	if is_relatedwork_ref(x):
		x[MIMETYPE] = RELATED_WORK_REF_POINTER_MIMETYES[0]
		
def internalization_mediaroll_pre_hook(k, x):
	if k == ITEMS and isinstance(x, MutableSequence):
		for item in x:
			internalization_ntiaudioref_pre_hook(None, item)
			internalization_ntivideoref_pre_hook(None, item)

def internalization_videoroll_pre_hook(k, x):
	mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
	if mimeType == "application/vnd.nextthought.ntivideoroll":
		x[MIMETYPE] = u"application/vnd.nextthought.videoroll"
	internalization_mediaroll_pre_hook(k, x)
internalization_audioroll_pre_hook = internalization_mediaroll_pre_hook

def internalization_courseoverview_pre_hook(k, x):
	if k == ITEMS and isinstance(x, MutableSequence):
		idx = 0
		while idx < len(x):
			item = x[idx]
			# Swizzle out our concrete mime types for refs.
			internalization_pollref_pre_hook(None, item)
			internalization_surveyref_pre_hook(None, item)
			internalization_ntiaudioref_pre_hook(None, item)
			internalization_ntivideoref_pre_hook(None, item)
			internalization_questionref_pre_hook(None, item)
			internalization_slidedeckref_pre_hook(None, item)
			internalization_assignmentref_pre_hook(None, item)
			internalization_ntitimelineref_pre_hook(None, item)
			internalization_questionsetref_pre_hook(None, item)
			internalization_relatedworkrefpointer_pre_hook(None, item)
			
			# do checks
			mimeType = item.get(MIMETYPE) if isinstance(item, Mapping) else None

			# handle discussions
			if mimeType == "application/vnd.nextthought.discussion":
				iden = item.get('id') or item.get(ID)
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
				elif not ntiids and not is_nti_course_bundle(iden):  # not yet ready
					del x[idx]
					continue
				else:
					internalization_discussionref_pre_hook(None, item)

			# handle media rolls
			if mimeType in ALL_MEDIA_ROLL_MIME_TYPES:
				internalization_mediaroll_pre_hook(ITEMS, item.get(ITEMS))

			# check next
			idx += 1

def internalization_lessonoverview_pre_hook(k, x):
	if k == ITEMS and isinstance(x, MutableSequence):
		for item in x:
			items = item.get(ITEMS) if isinstance(item, Mapping) else None
			if items is not None:
				internalization_courseoverview_pre_hook(ITEMS, items)
