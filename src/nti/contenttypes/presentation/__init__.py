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
from .interfaces import IGroupOverViewable

NTI_VIDEO = NTIVideo = u'NTIVideo'

NTI_SLIDE = NTISlide = u'NTISlide'
NTI_SLIDE_DECK = NTISlideDeck = u'NTISlideDeck'
NTI_SLIDE_VIDEO = NTISlideVideo = u'NTISlideVideo'

TIMELINE = NTI_TIMELINE = NTITimeline = 'Timeline'

RELATED_WORK = NTI_RELATED_WORK = 'RelatedWork'
RELATED_WORK_REF = NTI_RELATED_WORK_REF = 'RelatedWorkRef'

ENROLLED_COURSE_ROOT = 'EnrolledCourseRoot'
ENROLLED_COURSE_SECTION = 'EnrolledCourseSection'

DISCUSSION = 'discussion'
NTI_DISCUSSION = 'NTIDiscussion'
DISCUSSION_REF = NTI_DISCUSSION_REF = 'DiscussionRef'

DISCUSSION_REF_ENROLLED_COURSE_ROOT = DISCUSSION_REF + ':' + ENROLLED_COURSE_ROOT
DISCUSSION_REF_ENROLLED_COURSE_SECTION = DISCUSSION_REF + ':' + ENROLLED_COURSE_SECTION

COURSE_OVERVIEW_GROUP = 'CourseOverviewGroup'
NTI_COURSE_OVERVIEW_GROUP = 'NTICourseOverviewGroup'

LESSON_OVERVIEW = 'LessonOverview'
NTI_LESSON_OVERVIEW = 'NTILessonOverview'

GROUP_OVERVIEWABLE_INTERFACES = None

def _set_ifaces():
	global GROUP_OVERVIEWABLE_INTERFACES
	
	GROUP_OVERVIEWABLE_INTERFACES = set()
	m = sys.modules[IGroupOverViewable.__module__]
	
	def _item_predicate(item):
		result = bool(type(item) == interface.interface.InterfaceClass and \
					  issubclass(item, IGroupOverViewable) and \
					  item != IGroupOverViewable and \
					  item != IMediaRef)
		return result

	for _, item in inspect.getmembers(m, _item_predicate):
		GROUP_OVERVIEWABLE_INTERFACES.add(item)
	
	GROUP_OVERVIEWABLE_INTERFACES = tuple(GROUP_OVERVIEWABLE_INTERFACES)

_set_ifaces()
del _set_ifaces
