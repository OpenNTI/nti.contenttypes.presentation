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
from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.externalization import toExternalObject
from nti.externalization.interfaces import StandardExternalFields

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTISlide
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTITimeline
from .interfaces import INTISlideDeck
from .interfaces import INTIDiscussion
from .interfaces import INTISlideVideo
from .interfaces import INTIRelatedWork
from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIQuestionSetRef
from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewGroup

from . import NTI_SLIDE_DECK

CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
ITEMS = StandardExternalFields.ITEMS
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@interface.implementer( IExternalObject )
class _NTIBaseRenderExternalObject(object):

	def __init__( self, obj ):
		self.obj = obj

	def _do_toExternalObject( self, extDict ):
		return extDict

	def toExternalObject( self, *args, **kwargs ):
		extDict = toExternalObject( self.obj, name='')
		self._do_toExternalObject( extDict )
		return extDict

@interface.implementer( IExternalObject )
class _NTIMediaRenderExternalObject(_NTIBaseRenderExternalObject):

	media = alias('obj')
	
	def _do_toExternalObject( self, extDict ):
		if MIMETYPE in extDict:
			extDict[StandardExternalFields.CTA_MIMETYPE] = extDict.pop(MIMETYPE)
			
		if CREATOR in extDict:
			extDict[u'creator'] = extDict.pop(CREATOR)
		
		for name in (CLASS, u'DCDescription', u'DCTitle', NTIID):
			extDict.pop(name, None)

		for source in extDict.get('sources') or ():
			source.pop(MIMETYPE, None)
			source.pop(StandardExternalFields.CLASS, None)
		
		for transcript in extDict.get('transcripts') or ():
			transcript.pop(MIMETYPE, None)
			transcript.pop(StandardExternalFields.CLASS, None)		
		return extDict

@component.adapter( INTIVideo )
class _NTIVideoRenderExternalObject(_NTIMediaRenderExternalObject):

	def _do_toExternalObject( self, extDict ):
		extDict = super(_NTIVideoRenderExternalObject, self)._do_toExternalObject(extDict)

		if 'closed_caption' in extDict:
			extDict[u'closedCaptions'] = extDict.pop('closed_caption')
			
		for name in ('poster', 'label', 'subtitle'):
			if name in extDict and not extDict[name]:
				del extDict[name]	

		return extDict

@component.adapter( INTIAudio )
class _NTIAudioRenderExternalObject(_NTIMediaRenderExternalObject):
	pass

@component.adapter( INTIVideoRef )
class _NTIVideoRefRenderExternalObject(_NTIBaseRenderExternalObject):
	
	def _do_toExternalObject( self, extDict ):
		if MIMETYPE in extDict:
			extDict[MIMETYPE] = u"application/vnd.nextthought.ntivideo"
		extDict[u"visibility"] = u"everyone"

@component.adapter( INTIAudioRef )
class _NTIAudioRefRenderExternalObject(_NTIBaseRenderExternalObject):
	
	def _do_toExternalObject( self, extDict ):
		if MIMETYPE in extDict:
			extDict[MIMETYPE] = u"application/vnd.nextthought.ntiaudio"
		extDict[u"visibility"] = u"everyone"

@interface.implementer( IExternalObject )
class _NTIBaseSlideExternalObject(_NTIBaseRenderExternalObject):

	slide = alias('obj')
	
	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict[u'class'] = (extDict.pop(CLASS) or u'').lower()
		
		if CREATOR in extDict:
			extDict[u'creator'] = extDict.pop(CREATOR)

		if 'description' in extDict and not extDict['description']:
			extDict.pop('description') 

		return extDict

@component.adapter( INTISlide )
class _NTISlideRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject( self, extDict ):
		super(_NTISlideRenderExternalObject, self)._do_toExternalObject(extDict)

		for name in ("slidevideostart", "slidevideoend", "slidenumber"):
			value = extDict.get(name)
			if value is not None and not isinstance(value, six.string_types):
				extDict[name] = str(value)

		return extDict

@component.adapter( INTISlideVideo )
class _NTISlideVideoRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject( self, extDict ):
		super(_NTISlideVideoRenderExternalObject, self)._do_toExternalObject(extDict)
			
		if 'video_ntiid' in extDict:
			extDict[u'video-ntiid'] = extDict.pop('video_ntiid') 

		return extDict

@component.adapter( INTISlideDeck )
class _NTISlideDeckRenderExternalObject(_NTIBaseSlideExternalObject):

	def toExternalObject( self, *args, **kwargs ):
		extDict = LocatedExternalDict()
		extDict[u'title'] = self.slide.title
		extDict[u'ntiid'] = self.slide.ntiid
		extDict[u'creator'] = self.slide.creator
		extDict[MIMETYPE] = self.slide.mimeType
		extDict[u'class'] = NTI_SLIDE_DECK.lower()
		extDict[u'slidedeckid'] = self.slide.slidedeckid
		extDict[u'Slides'] = [toExternalObject(x, name='render') for x in self.slide.slides]
		extDict[u'Videos'] = [toExternalObject(x, name='render') for x in self.slide.videos]
		return extDict

@component.adapter( INTITimeline )
class _NTITimelineRenderExternalObject(_NTIBaseRenderExternalObject):

	timeline = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if 'description' in extDict:
			extDict[u'desc'] = extDict.pop('description')
		return extDict
		
@component.adapter( INTIRelatedWork )
class _NTIRelatedWorkRenderExternalObject(_NTIBaseRenderExternalObject):

	related = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if CREATOR in extDict:
			extDict[u'creator'] = extDict.pop(CREATOR)
		if 'description' in extDict:
			extDict[u'desc'] = extDict.pop('description')
		if 'target' in extDict:
			extDict[u'target-NTIID'] = extDict[u'target-ntiid'] = extDict.pop('target')
		if 'type' in extDict:
			extDict[u'targetMimeType'] = extDict['type']
		extDict[u"visibility"] = u"everyone"
		return extDict

@component.adapter( INTIDiscussion )
class _NTIDiscussionRenderExternalObject(_NTIBaseRenderExternalObject):

	related = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[NTIID] = extDict.pop('target')
		extDict[MIMETYPE] = 'application/vnd.nextthought.discussion'  #legacy
		return extDict

@component.adapter( INTIAssignmentRef )
class _NTIAssignmentRefRenderExternalObject(_NTIBaseRenderExternalObject):

	assignment = alias('obj')

	def _do_toExternalObject( self, extDict ):
		extDict[CLASS] = 'Assignment' # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.assessment.assignment'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		if 'containerId' in extDict:
			extDict[u'ContainerId'] = extDict.pop('containerId')
		return extDict

@component.adapter( INTIQuestionSetRef )
class _NTIQuestionSetRefRenderExternalObject(_NTIBaseRenderExternalObject):

	question_set = alias('obj')

	def _do_toExternalObject( self, extDict ):
		extDict[CLASS] = 'QuestionSet' # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.naquestionset'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		if 'question_count' in extDict:
			extDict[u'question-count'] = str(extDict.pop('question_count'))
		return extDict

@component.adapter( INTIQuestionRef )
class _NTIQuestionRefRenderExternalObject(_NTIBaseRenderExternalObject):

	question = alias('obj')

	def _do_toExternalObject( self, extDict ):
		extDict[CLASS] = 'Question' # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.naquestion'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict[u'Target-NTIID'] = extDict.pop('target')
		return extDict

@component.adapter( INTICourseOverviewGroup )
class _NTICourseOverviewGroupRenderExternalObject(_NTIBaseRenderExternalObject):

	course = alias('obj')

	def toExternalObject( self, *args, **kwargs ):
		extDict = LocatedExternalDict()
		extDict[NTIID] = self.course.ntiid
		extDict[MIMETYPE] = self.course.mimeType
		extDict[u'title'] = self.course.title
		extDict[u'accentColor'] = self.course.color
		extDict[ITEMS] = [toExternalObject(x, name='render') for x in self.course.items or ()]
		return extDict

@component.adapter( INTILessonOverview )
class _NTILessonOverviewRenderExternalObject(_NTIBaseRenderExternalObject):

	lesson = alias('obj')

	def toExternalObject( self, *args, **kwargs ):
		extDict = LocatedExternalDict()
		extDict[NTIID] = self.lesson.ntiid
		extDict[MIMETYPE] = self.lesson.mimeType
		extDict[u'title'] = self.lesson.title
		extDict[ITEMS] = [toExternalObject(x, name='render') for x in self.lesson.items or ()]
		return extDict