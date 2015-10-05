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

from .interfaces import IMediaRef
from .interfaces import INTIMedia
from .interfaces import INTIInquiryRef
from .interfaces import INTIMediaSource
from .interfaces import INTIAssessmentRef
from .interfaces import IGroupOverViewable
from .interfaces import IPresentationAsset

NTI_VIDEO = NTIVideo = u'NTIVideo'

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

GROUP_OVERVIEWABLE_INTERFACES = None
ALL_PRESENTATION_ASSETS_INTERFACES = None

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
					  item not in (IMediaRef, INTIAssessmentRef, INTIInquiryRef))
		return result

	def _presentationasset_item_predicate(item):
		result = bool(type(item) == interface.interface.InterfaceClass and \
					  issubclass(item, IPresentationAsset) and \
					  item != IPresentationAsset and \
					  item not in (IMediaRef, INTIAssessmentRef, INTIInquiryRef,
								   INTIMediaSource, INTIMedia))
		return result

	for _, item in inspect.getmembers(m, _overview_item_predicate):
		GROUP_OVERVIEWABLE_INTERFACES.add(item)

	for _, item in inspect.getmembers(m, _presentationasset_item_predicate):
		ALL_PRESENTATION_ASSETS_INTERFACES.add(item)

	GROUP_OVERVIEWABLE_INTERFACES = tuple(GROUP_OVERVIEWABLE_INTERFACES)
	ALL_PRESENTATION_ASSETS_INTERFACES = tuple(ALL_PRESENTATION_ASSETS_INTERFACES)

_set_ifaces()
del _set_ifaces
