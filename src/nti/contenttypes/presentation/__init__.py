#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys
import inspect

from zope import interface

from zope.interface.interfaces import IMethod

from nti.schema.jsonschema import TAG_HIDDEN_IN_UI

from .interfaces import IMediaRef
from .interfaces import INTIAudio
from .interfaces import INTIMedia
from .interfaces import INTISlide
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTITimeline
from .interfaces import INTIMediaRoll
from .interfaces import INTISlideDeck
from .interfaces import INTIInquiryRef
from .interfaces import INTISlideVideo
from .interfaces import INTIMediaSource
from .interfaces import INTIMediaRollRef
from .interfaces import INTIAssessmentRef
from .interfaces import INTIRelatedWorkRef
from .interfaces import IGroupOverViewable
from .interfaces import IPresentationAsset

NTI_AUDIO_REF = 'NTIAudioRef'
NTI_VIDEO_REF = 'NTIVideoRef'

NTI_VIDEO = NTIVideo = u'NTIVideo'
NTI_AUDIO = NTIAudio = u'NTIAudio'

NTI_POLL_REF = 'NTIPollRef'
NTI_SURVEY_REF = 'NTISurveyRef'

NTI_QUESTION_REF = 'NTIQuestionRef'
NTI_ASSIGNMENT_REF = 'NTIAssignmentRef'
NTI_QUESTION_SET_REF = 'NTIQuestionSetRef'

NTI_SLIDE = NTISlide = u'NTISlide'
NTI_SLIDE_DECK = NTISlideDeck = u'NTISlideDeck'
NTI_SLIDE_VIDEO = NTISlideVideo = u'NTISlideVideo'

JSON_TIMELINE = u'JSON:Timeline'
TIMELINE = NTI_TIMELINE = NTITimeline = u'Timeline'

RELATED_WORK = NTI_RELATED_WORK = 'RelatedWork'
RELATED_WORK_REF = NTI_RELATED_WORK_REF = 'RelatedWorkRef'

ENROLLED_COURSE_ROOT = 'EnrolledCourseRoot'
ENROLLED_COURSE_SECTION = 'EnrolledCourseSection'

DISCUSSION = u'discussion'
NTI_DISCUSSION = u'NTIDiscussion'
DISCUSSION_REF = NTI_DISCUSSION_REF = u'DiscussionRef'

NTI_COURSE_BUNDLE = u'nti-course-bundle'
NTI_COURSE_BUNDLE_TYPE = u'NTICourseBundle'
NTI_COURSE_BUNDLE_REF = "%s://" % NTI_COURSE_BUNDLE

DISCUSSION_REF_ENROLLED_COURSE_ROOT = DISCUSSION_REF + ':' + ENROLLED_COURSE_ROOT
DISCUSSION_REF_ENROLLED_COURSE_SECTION = DISCUSSION_REF + ':' + ENROLLED_COURSE_SECTION

COURSE_OVERVIEW_GROUP = u'CourseOverviewGroup'
NTI_COURSE_OVERVIEW_GROUP = u'NTICourseOverviewGroup'

COURSE_OVERVIEW_SPACER = u'CourseOverviewSpacer'
NTI_COURSE_OVERVIEW_SPACER = u'NTICourseOverviewSpacer'

LESSON_OVERVIEW = u'LessonOverview'
NTI_LESSON_OVERVIEW = u'NTILessonOverview'

NTI_AUDIO_ROLL_REF = 'NTIAudioRollRef'
NTI_VIDEO_ROLL_REF = 'NTIVideoRollRef'

AUDIO_MIMETYES = ('application/vnd.nextthought.ntiaudio',)
VIDEO_MIMETYES = ('application/vnd.nextthought.ntivideo',)
AUDIO_REF_MIMETYES = ('application/vnd.nextthought.ntiaudioref',)
VIDEO_REF_MIMETYES = ('application/vnd.nextthought.ntivideoref',)
RELATED_WORK_REF_MIMETYES = ('application/vnd.nextthought.relatedworkref',)
LESSON_OVERVIEW_MIMETYES = ('application/vnd.nextthought.ntilessonoverview',)
COURSE_OVERVIEW_GROUP_MIMETYES = ('application/vnd.nextthought.nticourseoverviewgroup',)

AUDIO_ROLL_MIMETYES = ('application/vnd.nextthought.ntiaudioroll','application/vnd.nextthought.audioroll')
VIDEO_ROLL_MIMETYES = ('application/vnd.nextthought.ntivideoroll','application/vnd.nextthought.videoroll')
ALL_MEDIA_ROLL_MIME_TYPES = AUDIO_ROLL_MIMETYES + VIDEO_ROLL_MIMETYES

MEDIA_ROLL_REF_MIMETYES = ('application/vnd.nextthought.ntimediarollref',)
AUDIO_ROLL_REF_MIMETYES = ('application/vnd.nextthought.ntiaudiorollref',)
VIDEO_ROLL_REF_MIMETYES = ('application/vnd.nextthought.ntivideorollref',)

POLL_REF_MIMETYES = ('application/vnd.nextthought.pollref', 'application/vnd.nextthought.napoll')
TIMELINE_MIMETYES = ('application/vnd.nextthought.ntitimeline', 'application/vnd.nextthought.timeline')
SURVEY_REF_MIMETYES = ('application/vnd.nextthought.surveyref', 'application/vnd.nextthought.surveyref')
QUESTION_REF_MIMETYES = ('application/vnd.nextthought.questionref', 'application/vnd.nextthought.naquestion')
ASSIGNMENT_REF_MIMETYES = ('application/vnd.nextthought.assignmentref', 'application/vnd.nextthought.assignment')
DISCUSSION_REF_MIMETYES = ('application/vnd.nextthought.discussionref', 'application/vnd.nextthought.discussion')
QUESTIONSET_REF_MIMETYES = ('application/vnd.nextthought.questionsetref', 'application/vnd.nextthought.naquestionset')

PACKAGE_CONTAINER_INTERFACES = (INTIAudio, INTIVideo, INTITimeline, INTIRelatedWorkRef,
								INTISlideDeck, INTISlide, INTISlideVideo)

MEDIA_INTERFACES = (INTIAudio, INTIVideo, INTISlideDeck, INTIAudioRef, INTIVideoRef)

REF_INTERFACES = (IMediaRef, INTIAssessmentRef, INTIInquiryRef)

GROUP_OVERVIEWABLE_INTERFACES = None
ALL_PRESENTATION_ASSETS_INTERFACES = None

def iface_of_asset(item):
	for iface in ALL_PRESENTATION_ASSETS_INTERFACES:
		if iface.providedBy(item):
			return iface
	return None

def _set_ifaces():
	global GROUP_OVERVIEWABLE_INTERFACES
	global ALL_PRESENTATION_ASSETS_INTERFACES

	GROUP_OVERVIEWABLE_INTERFACES = set()
	ALL_PRESENTATION_ASSETS_INTERFACES = set()

	m = sys.modules[IGroupOverViewable.__module__]

	def _overview_item_predicate(item):
		result = bool(type(item) == interface.interface.InterfaceClass and \
					  issubclass(item, IGroupOverViewable) and \
					  item != IGroupOverViewable and \
					  item not in (IMediaRef, INTIAssessmentRef, INTIInquiryRef,
								   INTIMediaRollRef))
		return result

	def _presentationasset_item_predicate(item):
		result = bool(type(item) == interface.interface.InterfaceClass and \
					  issubclass(item, IPresentationAsset) and \
					  item != IPresentationAsset and \
					  item not in (IMediaRef, INTIAssessmentRef, INTIInquiryRef,
								   INTIMediaSource, INTIMedia, INTIMediaRoll,
								   INTIMediaRollRef))
		return result

	for _, item in inspect.getmembers(m, _overview_item_predicate):
		GROUP_OVERVIEWABLE_INTERFACES.add(item)

	for _, item in inspect.getmembers(m, _presentationasset_item_predicate):
		ALL_PRESENTATION_ASSETS_INTERFACES.add(item)

	GROUP_OVERVIEWABLE_INTERFACES = tuple(GROUP_OVERVIEWABLE_INTERFACES)
	ALL_PRESENTATION_ASSETS_INTERFACES = tuple(ALL_PRESENTATION_ASSETS_INTERFACES)
	
	# set ui settings
	for iSchema in ALL_PRESENTATION_ASSETS_INTERFACES:
		for k, v in iSchema.namesAndDescriptions(all=True):
			if IMethod.providedBy(v) or v.queryTaggedValue(TAG_HIDDEN_IN_UI) is not None:
				continue
			iSchema[k].setTaggedValue(TAG_HIDDEN_IN_UI, True)

_set_ifaces()
del _set_ifaces
