#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

from zope import component
from zope import interface

from nti.common.property import alias

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import IInternalObjectIO
from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.externalization import toExternalObject

from nti.externalization.autopackage import AutoPackageSearchingScopedInterfaceObjectIO

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTISlide
from .interfaces import INTIPollRef
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTITimeline
from .interfaces import INTISlideDeck
from .interfaces import INTISurveyRef
from .interfaces import INTISlideVideo
from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIDiscussionRef
from .interfaces import INTIQuestionSetRef
from .interfaces import INTILessonOverview
from .interfaces import INTIRelatedWorkRef
from .interfaces import INTICourseOverviewGroup
from .interfaces import INTICourseOverviewSpacer

from . import NTI_SLIDE_DECK

OID = StandardExternalFields.OID
CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
ITEMS = StandardExternalFields.ITEMS
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE
CREATED_TIME = StandardExternalFields.CREATED_TIME
LAST_MODIFIED = StandardExternalFields.LAST_MODIFIED

@interface.implementer(IExternalObject)
class _NTIBaseRenderExternalObject(object):

	def __init__(self, obj):
		self.obj = obj

	def _do_toExternalObject(self, extDict):
		extDict.pop(OID, None)
		extDict.pop(CREATED_TIME, None)
		extDict.pop(LAST_MODIFIED, None)
		return extDict

	def toExternalObject(self, *args, **kwargs):
		extDict = toExternalObject(self.obj, name='')
		self._do_toExternalObject(extDict)
		return extDict

@interface.implementer(IExternalObject)
class _NTIMediaRenderExternalObject(_NTIBaseRenderExternalObject):

	media = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIMediaRenderExternalObject, self)._do_toExternalObject(extDict)
		if MIMETYPE in extDict:
			extDict[StandardExternalFields.CTA_MIMETYPE] = extDict[MIMETYPE]  # legacy

		if CREATOR in extDict:
			extDict[u'creator'] = extDict[CREATOR] # legacy

		if 'ntiid' in extDict and NTIID not in extDict:
			extDict[NTIID] = extDict['ntiid'] # alias
	
		for name in (u'DCDescription', u'DCTitle'):
			extDict.pop(name, None)

		for source in extDict.get('sources') or ():
			source.pop(CREATED_TIME, None)
			source.pop(LAST_MODIFIED, None)

		for transcript in extDict.get('transcripts') or ():
			transcript.pop(CREATED_TIME, None)
			transcript.pop(LAST_MODIFIED, None)
		return extDict

@component.adapter(INTIVideo)
class _NTIVideoRenderExternalObject(_NTIMediaRenderExternalObject):

	def _do_toExternalObject(self, extDict):
		super(_NTIVideoRenderExternalObject, self)._do_toExternalObject(extDict)

		if 'closed_caption' in extDict:
			extDict[u'closedCaptions'] = extDict['closed_caption'] # legacy

		for name in ('poster', 'label', 'subtitle'):
			if name in extDict and not extDict[name]:
				del extDict[name]

		title = extDict.get('title')
		if title and not extDict.get('label'):
			extDict['label'] = title

		return extDict

@component.adapter(INTIAudio)
class _NTIAudioRenderExternalObject(_NTIMediaRenderExternalObject):
	pass

@component.adapter(INTIVideoRef)
class _NTIVideoRefRenderExternalObject(_NTIBaseRenderExternalObject):

	def _do_toExternalObject(self, extDict):
		super(_NTIVideoRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if MIMETYPE in extDict:
			extDict[MIMETYPE] = u"application/vnd.nextthought.ntivideo"

@component.adapter(INTIAudioRef)
class _NTIAudioRefRenderExternalObject(_NTIBaseRenderExternalObject):

	def _do_toExternalObject(self, extDict):
		super(_NTIAudioRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if MIMETYPE in extDict:
			extDict[MIMETYPE] = u"application/vnd.nextthought.ntiaudio"

@interface.implementer(IExternalObject)
class _NTIBaseSlideExternalObject(_NTIBaseRenderExternalObject):

	slide = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIBaseSlideExternalObject, self)._do_toExternalObject(extDict)
		if CLASS in extDict:
			extDict[u'class'] = (extDict.get(CLASS) or u'').lower() # legacy

		if CREATOR in extDict:
			extDict[u'creator'] = extDict[CREATOR] # alias

		if 'description' in extDict and not extDict['description']:
			extDict.pop('description')

		return extDict

@component.adapter(INTISlide)
class _NTISlideRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject(self, extDict):
		super(_NTISlideRenderExternalObject, self)._do_toExternalObject(extDict)

		for name in ("slidevideostart", "slidevideoend", "slidenumber"):
			value = extDict.get(name)
			if value is not None and not isinstance(value, six.string_types):
				extDict[name] = str(value)

		return extDict

@component.adapter(INTISlideVideo)
class _NTISlideVideoRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject(self, extDict):
		super(_NTISlideVideoRenderExternalObject, self)._do_toExternalObject(extDict)

		if 'video_ntiid' in extDict:
			extDict[u'video-ntiid'] = extDict['video_ntiid'] # legacy

		return extDict

@component.adapter(INTISlideDeck)
class _NTISlideDeckRenderExternalObject(_NTIBaseSlideExternalObject):

	def toExternalObject(self, *args, **kwargs):
		extDict = LocatedExternalDict()
		extDict[u'title'] = self.slide.title
		extDict[u'creator'] = self.slide.creator
		extDict[MIMETYPE] = self.slide.mimeType
		extDict[u'slidedeckid'] = self.slide.slidedeckid
		extDict[u'ntiid'] = extDict[NTIID] = self.slide.ntiid
		extDict[CLASS] = extDict[u'class'] = NTI_SLIDE_DECK.lower()
		extDict[u'Slides'] = [toExternalObject(x, name='render', decorate=False)
							  for x in self.slide.slides]
		extDict[u'Videos'] = [toExternalObject(x, name='render', decorate=False) 
							  for x in self.slide.videos]
		return extDict

@component.adapter(INTITimeline)
class _NTITimelineRenderExternalObject(_NTIBaseRenderExternalObject):

	timeline = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTITimelineRenderExternalObject, self)._do_toExternalObject(extDict)
		if 'description' in extDict:
			extDict[u'desc'] = extDict['description']
		if 'suggested_inline' in extDict:
			if extDict['suggested_inline'] is None:
				extDict.pop('suggested_inline')
			else:
				extDict['suggested-inline'] = extDict['suggested_inline'] # legacy
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict['ntiid'] # legacy
		return extDict

@component.adapter(INTIRelatedWorkRef)
class _NTIRelatedWorkRefRenderExternalObject(_NTIBaseRenderExternalObject):

	related = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIRelatedWorkRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if CREATOR in extDict:
			extDict[u'creator'] = extDict[CREATOR] # legacy
		if 'description' in extDict:
			extDict[u'desc'] = extDict['description'] # legacy
		if 'target' in extDict:
			extDict[u'target-NTIID'] = extDict[u'target-ntiid'] = extDict['target'] # legacy
		if 'type' in extDict:
			extDict[u'targetMimeType'] = extDict['type']
		return extDict
_NTIRelatedWorkRenderExternalObject = _NTIRelatedWorkRefRenderExternalObject

@component.adapter(INTIDiscussionRef)
class _NTIDiscussionRefRenderExternalObject(_NTIBaseRenderExternalObject):

	discussion = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIDiscussionRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[NTIID] = extDict.pop('target')
		extDict[MIMETYPE] = 'application/vnd.nextthought.discussion'  # legacy
		return extDict

@component.adapter(INTIAssignmentRef)
class _NTIAssignmentRefRenderExternalObject(_NTIBaseRenderExternalObject):

	assignment = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIAssignmentRefRenderExternalObject, self)._do_toExternalObject(extDict)
		extDict[CLASS] = 'Assignment'  # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.assessment.assignment'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		if 'containerId' in extDict:
			extDict[u'ContainerId'] = extDict.pop('containerId')
		return extDict

@component.adapter(INTISurveyRef)
class _NTISurveyRefRenderExternalObject(_NTIBaseRenderExternalObject):

	survey = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTISurveyRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		if 'question_count' in extDict:
			extDict[u'question-count'] = str(extDict.pop('question_count'))
		return extDict

@component.adapter(INTIPollRef)
class _NTIPollRefRenderExternalObject(_NTIBaseRenderExternalObject):

	survey = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIPollRefRenderExternalObject, self)._do_toExternalObject(extDict)
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		return extDict

@component.adapter(INTIQuestionSetRef)
class _NTIQuestionSetRefRenderExternalObject(_NTIBaseRenderExternalObject):

	question_set = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIQuestionSetRefRenderExternalObject, self)._do_toExternalObject(extDict)
		extDict[CLASS] = 'QuestionSet'  # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.naquestionset'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		if 'question_count' in extDict:
			extDict[u'question-count'] = str(extDict.pop('question_count'))
		return extDict

@component.adapter(INTIQuestionRef)
class _NTIQuestionRefRenderExternalObject(_NTIBaseRenderExternalObject):

	question = alias('obj')

	def _do_toExternalObject(self, extDict):
		super(_NTIQuestionRefRenderExternalObject, self)._do_toExternalObject(extDict)
		extDict[CLASS] = 'Question'  # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.naquestion'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		return extDict

@component.adapter(INTICourseOverviewSpacer)
class _NTICourseOverviewSpacerRenderExternalObject(_NTIBaseRenderExternalObject):

	spacer = alias('obj')

	def toExternalObject(self, *args, **kwargs):
		extDict = LocatedExternalDict()
		extDict[MIMETYPE] = self.spacer.mimeType
		return extDict

@component.adapter(INTICourseOverviewGroup)
class _NTICourseOverviewGroupRenderExternalObject(_NTIBaseRenderExternalObject):

	group = alias('obj')

	def toExternalObject(self, *args, **kwargs):
		extDict = LocatedExternalDict()
		extDict[NTIID] = self.group.ntiid
		extDict[u'title'] = self.group.title
		extDict[MIMETYPE] = self.group.mimeType
		extDict[u'accentColor'] = self.group.color
		extDict[CLASS] = self.group.__external_class_name__
		extDict[ITEMS] = [toExternalObject(x, name='render', decorate=False)
						  for x in self.group]
		return extDict

@interface.implementer(IInternalObjectIO)
class _NTICourseOverviewGroupInternalObjectIO(AutoPackageSearchingScopedInterfaceObjectIO):

	_excluded = {ITEMS}
	_excluded_out_ivars_ = _excluded | AutoPackageSearchingScopedInterfaceObjectIO._excluded_out_ivars_

	@classmethod
	def _ap_enumerate_externalizable_root_interfaces(cls, pa_interfaces):
		return (pa_interfaces.INTICourseOverviewGroup,)

	@classmethod
	def _ap_enumerate_module_names(cls):
		return ('group',)

	def toExternalObject(self, *args, **kwargs):
		result = super(_NTICourseOverviewGroupInternalObjectIO, self).toExternalObject(*args, **kwargs)
		result[ITEMS] = [toExternalObject(x) for x in self._ext_self]
		return result
_NTICourseOverviewGroupInternalObjectIO.__class_init__()

@component.adapter(INTILessonOverview)
class _NTILessonOverviewRenderExternalObject(_NTIBaseRenderExternalObject):

	lesson = alias('obj')

	def toExternalObject(self, *args, **kwargs):
		items = self.obj.items or ()
		extDict = LocatedExternalDict()
		extDict[NTIID] = self.obj.ntiid
		extDict[u'title'] = self.obj.title
		extDict[u'lesson'] = self.obj.lesson
		extDict[MIMETYPE] = self.obj.mimeType
		extDict[CLASS] = self.obj.__external_class_name__
		extDict[ITEMS] = [toExternalObject(x, name='render') for x in items]
		return extDict
