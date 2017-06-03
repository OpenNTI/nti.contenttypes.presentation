#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory(__name__)

import sys
import inspect

from zope import interface

from zope.interface.interfaces import IMethod

from nti.contenttypes.presentation.interfaces import IAssetRef
from nti.contenttypes.presentation.interfaces import IMediaRef
from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIMedia
from nti.contenttypes.presentation.interfaces import INTISlide
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIMediaRef
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import IConcreteAsset
from nti.contenttypes.presentation.interfaces import INTIInquiryRef
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import INTIDocketAsset
from nti.contenttypes.presentation.interfaces import INTIMediaSource
from nti.contenttypes.presentation.interfaces import INTIAssessmentRef
from nti.contenttypes.presentation.interfaces import IUserCreatedAsset
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef
from nti.contenttypes.presentation.interfaces import IGroupOverViewable
from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import ICoursePresentationAsset
from nti.contenttypes.presentation.interfaces import ILegacyPresentationAsset
from nti.contenttypes.presentation.interfaces import IPackagePresentationAsset
from nti.contenttypes.presentation.interfaces import IContentBackedPresentationAsset

from nti.schema.jsonschema import TAG_HIDDEN_IN_UI

#: Fields attribute
FIELDS = 'Fields'

#: Accepts attribute
ACCEPTS = 'Accepts'

#: Audio Ref NTIID type
NTI_AUDIO_REF = 'NTIAudioRef'

#: Video Ref NTIID type
NTI_VIDEO_REF = 'NTIVideoRef'

#: Audio Roll NTIID type
NTI_AUDIO_ROLL = 'NTIAudioRoll'

#: Video Roll NTIID type
NTI_VIDEO_ROLL = 'NTIVideoRoll'

#: Audio NTIID type
NTI_AUDIO = NTIAudio = u'NTIAudio'

#: Video NTIID type
NTI_VIDEO = NTIVideo = u'NTIVideo'

#: Transcript NTIID type
NTI_TRANSCRIPT = u'NTITranscript'

#: Audio source NTIID type
NTI_AUDIO_SOURCE = u'NTIAudioSource'

#: Video source NTIID type
NTI_VIDEO_SOURCE = u'NTIVideoSource'

#: Poll Ref NTIID type
NTI_POLL_REF = 'NTIPollRef'

#: Survey Ref NTIID type
NTI_SURVEY_REF = 'NTISurveyRef'

#: Question Ref NTIID type
NTI_QUESTION_REF = 'NTIQuestionRef'

#: Assigment Ref NTIID type
NTI_ASSIGNMENT_REF = 'NTIAssignmentRef'

#: QuestionSet Ref NTIID type
NTI_QUESTION_SET_REF = 'NTIQuestionSetRef'

#: Slide NTIID type
NTI_SLIDE = NTISlide = u'NTISlide'

#: Slide Deck NTIID type
NTI_SLIDE_DECK = NTISlideDeck = u'NTISlideDeck'

#: Slide Slide Video NTIID type
NTI_SLIDE_VIDEO = NTISlideVideo = u'NTISlideVideo'

#: SlideDeckRef NTIID type
NTI_SLIDE_DECK_REF = u'NTISlideDeckRef'

#: JSON Timeline NTIID type
JSON_TIMELINE = u'JSON:Timeline'

#: Timeline NTIID type
NTI_TIMELINE = u'NTITimeline'
TIMELINE = NTITimeline = u'Timeline'

#: SlideDeckRef NTIID type
NTI_TIMELIME_REF = u'NTITimeLineRef'

#: Related Work Ref NTIID type
RELATED_WORK_REF = 'RelatedWorkRef'
NTI_RELATED_WORK_REF = 'NTIRelatedWorkRef'
RELATED_WORK = NTI_RELATED_WORK = 'RelatedWork'

#: Related Workf Ref Pointer NTIID type
NTI_RELATED_WORK_REF_POINTER = u'NTIRelatedWorkRefPointer'

ENROLLED_COURSE_ROOT = 'EnrolledCourseRoot'
ENROLLED_COURSE_SECTION = 'EnrolledCourseSection'

DISCUSSION = u'discussion'
NTI_DISCUSSION = u'NTIDiscussion'
DISCUSSION_REF = NTI_DISCUSSION_REF = u'DiscussionRef'

NTI_COURSE_BUNDLE = u'nti-course-bundle'
NTI_COURSE_BUNDLE_TYPE = u'NTICourseBundle'
NTI_COURSE_BUNDLE_REF = "%s://" % NTI_COURSE_BUNDLE

DISCUSSION_REF_ENROLLED_COURSE_ROOT = DISCUSSION_REF + \
    ':' + ENROLLED_COURSE_ROOT
DISCUSSION_REF_ENROLLED_COURSE_SECTION = DISCUSSION_REF + \
    ':' + ENROLLED_COURSE_SECTION

COURSE_OVERVIEW_GROUP = u'CourseOverviewGroup'
NTI_COURSE_OVERVIEW_GROUP = u'NTICourseOverviewGroup'

COURSE_OVERVIEW_SPACER = u'CourseOverviewSpacer'
NTI_COURSE_OVERVIEW_SPACER = u'NTICourseOverviewSpacer'

LESSON_OVERVIEW = u'LessonOverview'
NTI_LESSON_OVERVIEW = u'NTILessonOverview'

NTI_LESSON_COMPLETION_CONSTRAINT = u'NTILessonCompletionConstraint'

PUBLICATION_CONSTRAINTS = u'PublicationConstraints'

SLIDE_MIME_TYPES = ('application/vnd.nextthought.slide',)
SLIDE_DECK_MIME_TYPES = ('application/vnd.nextthought.ntislidedeck',)
SLIDE_VIDEO_MIME_TYPES = ('application/vnd.nextthought.ntislidevideo',)
SLIDE_DECK_REF_MIME_TYPES = ('application/vnd.nextthought.ntislideckref',)

TIMELINE_MIME_TYPES = ('application/vnd.nextthought.ntitimeline',
                     'application/vnd.nextthought.timeline')
TIMELINE_REF_MIME_TYPES = ('application/vnd.nextthought.ntitimelineref',)

AUDIO_MIME_TYPES = ('application/vnd.nextthought.ntiaudio',)
VIDEO_MIME_TYPES = ('application/vnd.nextthought.ntivideo',)
AUDIO_REF_MIME_TYPES = ('application/vnd.nextthought.ntiaudioref',)
VIDEO_REF_MIME_TYPES = ('application/vnd.nextthought.ntivideoref',)

RELATED_WORK_REF_MIME_TYPES = ('application/vnd.nextthought.relatedworkref',)
RELATED_WORK_REF_POINTER_MIME_TYPES = ('application/vnd.nextthought.relatedworkrefpointer',)

LESSON_OVERVIEW_MIME_TYPES = ('application/vnd.nextthought.ntilessonoverview',)
COURSE_OVERVIEW_GROUP_MIME_TYPES = ('application/vnd.nextthought.nticourseoverviewgroup',)

AUDIO_ROLL_MIME_TYPES = ('application/vnd.nextthought.ntiaudioroll',
                         'application/vnd.nextthought.audioroll')
VIDEO_ROLL_MIME_TYPES = ('application/vnd.nextthought.videoroll',
                         'application/vnd.nextthought.ntivideoroll')
ALL_MEDIA_ROLL_MIME_TYPES = AUDIO_ROLL_MIME_TYPES + VIDEO_ROLL_MIME_TYPES

POLL_REF_MIME_TYPES = ('application/vnd.nextthought.pollref',
                       'application/vnd.nextthought.napoll')
SURVEY_REF_MIME_TYPES = ('application/vnd.nextthought.surveyref',
                         'application/vnd.nextthought.surveyref')
QUESTION_REF_MIME_TYPES = ('application/vnd.nextthought.questionref',
                           'application/vnd.nextthought.naquestion')
ASSIGNMENT_REF_MIME_TYPES = ('application/vnd.nextthought.assignmentref',
                             'application/vnd.nextthought.assignment')
DISCUSSION_REF_MIME_TYPES = ('application/vnd.nextthought.discussionref',
                             'application/vnd.nextthought.discussion')
QUESTIONSET_REF_MIME_TYPES = ('application/vnd.nextthought.questionsetref',
                              'application/vnd.nextthought.naquestionset')

ALL_MEDIA_INTERFACES = (INTIAudio, INTIVideo, INTISlideDeck, INTIAudioRef,
                        INTIVideoRef, INTIVideoRoll, INTIAudioRoll)

MEDIA_REF_INTERFACES = (INTIAudioRef, INTIVideoRef)

ALL_MIME_TYPES = None
COURSE_CONTAINER_INTERFACES = None
PACKAGE_CONTAINER_INTERFACES = None
GROUP_OVERVIEWABLE_INTERFACES = None
ALL_PRESENTATION_ASSETS_INTERFACES = None


def interface_of_asset(item):
    for iface in ALL_PRESENTATION_ASSETS_INTERFACES:
        if iface.providedBy(item):
            return iface
    return None
iface_of_asset = interface_of_asset


def _set_ifaces():
    global ALL_MIME_TYPES
    global COURSE_CONTAINER_INTERFACES
    global PACKAGE_CONTAINER_INTERFACES
    global GROUP_OVERVIEWABLE_INTERFACES
    global ALL_PRESENTATION_ASSETS_INTERFACES

    ALL_MIME_TYPES = set()
    COURSE_CONTAINER_INTERFACES = set()
    PACKAGE_CONTAINER_INTERFACES = set()
    GROUP_OVERVIEWABLE_INTERFACES = set()
    ALL_PRESENTATION_ASSETS_INTERFACES = set()

    module = sys.modules[IGroupOverViewable.__module__]

    # Ref interfaces that ARE NOT IMPLEMENTED
    NO_IMPL_REF_IFACES = (INTIMediaRef, INTIAssessmentRef, INTIInquiryRef,
                          INTIDocketAsset, IAssetRef)

    # Interfaces that ARE NOT IMPLEMENTED
    NO_IMPL_IFACES = NO_IMPL_REF_IFACES + (INTIMediaSource, INTIMedia,
                                           INTIMediaRoll, IConcreteAsset)

    def _package_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, IPackagePresentationAsset)
                      and item != IPackagePresentationAsset
                      and item not in (INTIMedia, INTIDocketAsset, IConcreteAsset))
        return result

    def _course_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, ICoursePresentationAsset)
                      and item != ICoursePresentationAsset
                      and item not in NO_IMPL_REF_IFACES)
        return result

    def _overview_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, IGroupOverViewable)
                      and item != IGroupOverViewable
                      and item not in NO_IMPL_REF_IFACES)
        return result

    def _presentationasset_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, IPresentationAsset)
                      and item != IPresentationAsset
                      and item != IUserCreatedAsset
                      and item != ICoursePresentationAsset
                      and item != ILegacyPresentationAsset
                      and item != IPackagePresentationAsset
                      and item != IContentBackedPresentationAsset
                      and item not in NO_IMPL_IFACES)
        return result

    for _, item in inspect.getmembers(module, _course_item_predicate):
        COURSE_CONTAINER_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _package_item_predicate):
        PACKAGE_CONTAINER_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _overview_item_predicate):
        GROUP_OVERVIEWABLE_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _presentationasset_item_predicate):
        ALL_PRESENTATION_ASSETS_INTERFACES.add(item)

    COURSE_CONTAINER_INTERFACES = tuple(COURSE_CONTAINER_INTERFACES)
    PACKAGE_CONTAINER_INTERFACES = tuple(PACKAGE_CONTAINER_INTERFACES)
    GROUP_OVERVIEWABLE_INTERFACES = tuple(GROUP_OVERVIEWABLE_INTERFACES)
    ALL_PRESENTATION_ASSETS_INTERFACES = tuple(ALL_PRESENTATION_ASSETS_INTERFACES)

    # set ui settings
    for iSchema in ALL_PRESENTATION_ASSETS_INTERFACES:
        for k, v in iSchema.namesAndDescriptions(all=True):
            if IMethod.providedBy(v) or v.queryTaggedValue(TAG_HIDDEN_IN_UI) is not None:
                continue
            iSchema[k].setTaggedValue(TAG_HIDDEN_IN_UI, True)

    # capture all mime types
    def _tuples_item_predicate(item):
        return type(item) == tuple

    frame = sys._getframe(1)
    module = sys.modules[frame.f_globals['__name__']]
    for name, item in inspect.getmembers(module, _tuples_item_predicate):
        if name.endswith('MIME_TYPES'):
            ALL_MIME_TYPES.update(str(x) for x in item)
    ALL_MIME_TYPES = tuple(sorted(ALL_MIME_TYPES))


_set_ifaces()
del _set_ifaces

# make sure all constants have been loaded
from nti.contenttypes.presentation._patch import patch
patch()
del patch
