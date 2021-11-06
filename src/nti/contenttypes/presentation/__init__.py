#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=global-statement,no-member

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

from nti.schema.interfaces import find_most_derived_interface

from nti.schema.jsonschema import TAG_HIDDEN_IN_UI

#: NTI provider
NTI = u'NTI'

#: Fields attribute
FIELDS = u'Fields'

#: Accepts attribute
ACCEPTS = u'Accepts'

#: Audio Ref NTIID type
NTI_AUDIO_REF = u'NTIAudioRef'

#: Video Ref NTIID type
NTI_VIDEO_REF = u'NTIVideoRef'

#: Audio Roll NTIID type
NTI_AUDIO_ROLL = u'NTIAudioRoll'

#: Video Roll NTIID type
NTI_VIDEO_ROLL = u'NTIVideoRoll'

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
NTI_POLL_REF = u'NTIPollRef'

#: Survey Ref NTIID type
NTI_SURVEY_REF = u'NTISurveyRef'

#: Question Ref NTIID type
NTI_QUESTION_REF = u'NTIQuestionRef'

#: Assigment Ref NTIID type
NTI_ASSIGNMENT_REF = u'NTIAssignmentRef'

#: QuestionSet Ref NTIID type
NTI_QUESTION_SET_REF = u'NTIQuestionSetRef'

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
RELATED_WORK_REF = u'RelatedWorkRef'
NTI_RELATED_WORK_REF = u'NTIRelatedWorkRef'
RELATED_WORK = NTI_RELATED_WORK = u'RelatedWork'

#: Related Workf Ref Pointer NTIID type
NTI_RELATED_WORK_REF_POINTER = u'NTIRelatedWorkRefPointer'

NTI_CALENDAR_EVENT_REF = u'NTICalendarEventRef'

ENROLLED_COURSE_ROOT = u'EnrolledCourseRoot'
ENROLLED_COURSE_SECTION = u'EnrolledCourseSection'

DISCUSSION = u'discussion'
NTI_DISCUSSION = u'NTIDiscussion'
DISCUSSION_REF = NTI_DISCUSSION_REF = u'DiscussionRef'

NTI_COURSE_BUNDLE = u'nti-course-bundle'
NTI_COURSE_BUNDLE_TYPE = u'NTICourseBundle'
NTI_COURSE_BUNDLE_REF = u"%s://" % NTI_COURSE_BUNDLE

DISCUSSION_REF_ENROLLED_COURSE_ROOT = DISCUSSION_REF + ':' + ENROLLED_COURSE_ROOT
DISCUSSION_REF_ENROLLED_COURSE_SECTION = DISCUSSION_REF + ':' + ENROLLED_COURSE_SECTION

COURSE_OVERVIEW_GROUP = u'CourseOverviewGroup'
NTI_COURSE_OVERVIEW_GROUP = u'NTICourseOverviewGroup'

COURSE_OVERVIEW_SPACER = u'CourseOverviewSpacer'
NTI_COURSE_OVERVIEW_SPACER = u'NTICourseOverviewSpacer'

LESSON_OVERVIEW = u'LessonOverview'
NTI_LESSON_OVERVIEW = u'NTILessonOverview'

NTI_LESSON_COMPLETION_CONSTRAINT = u'NTILessonCompletionConstraint'

PUBLICATION_CONSTRAINTS = u'PublicationConstraints'

TEXT_VTT_MIMETYPE = "text/vtt"

NTI_TRANSCRIPT_MIMETYPE = 'application/vnd.nextthought.ntitranscript'

SLIDE_MIME_TYPES = ('application/vnd.nextthought.slide', # legacy
                    'application/vnd.nextthought.ntislide')
SLIDE_DECK_MIME_TYPES = ('application/vnd.nextthought.ntislidedeck',)
SLIDE_VIDEO_MIME_TYPES = ('application/vnd.nextthought.ntislidevideo',)
SLIDE_DECK_REF_MIME_TYPES = ('application/vnd.nextthought.ntislidedeckref',)

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
VIDEO_ROLL_MIME_TYPES = ('application/vnd.nextthought.videoroll', # legacy
                         'application/vnd.nextthought.ntivideoroll')
ALL_MEDIA_ROLL_MIME_TYPES = AUDIO_ROLL_MIME_TYPES + VIDEO_ROLL_MIME_TYPES

POLL_REF_MIME_TYPES = ('application/vnd.nextthought.pollref',
                       'application/vnd.nextthought.napoll')
SURVEY_REF_MIME_TYPES = ('application/vnd.nextthought.surveyref',)
QUESTION_REF_MIME_TYPES = ('application/vnd.nextthought.questionref',
                           'application/vnd.nextthought.naquestion')
ASSIGNMENT_REF_MIME_TYPES = ('application/vnd.nextthought.assignmentref',
                             'application/vnd.nextthought.assignment')
DISCUSSION_REF_MIME_TYPES = ('application/vnd.nextthought.discussionref',
                             'application/vnd.nextthought.discussion')
QUESTIONSET_REF_MIME_TYPES = ('application/vnd.nextthought.questionsetref',
                              'application/vnd.nextthought.naquestionset')

CALENDAR_EVENT_REF_MIME_TYPES = ('application/vnd.nextthought.nticalendareventref',)

ALL_MEDIA_INTERFACES = (INTIAudio, INTIVideo, INTISlideDeck, INTIAudioRef,
                        INTIVideoRef, INTIVideoRoll, INTIAudioRoll)

MEDIA_REF_INTERFACES = (INTIAudioRef, INTIVideoRef)

MARKER_INTERFACES = None
ALL_PRESENTATION_MIME_TYPES = None
COURSE_CONTAINER_INTERFACES = None
PACKAGE_CONTAINER_INTERFACES = None
GROUP_OVERVIEWABLE_INTERFACES = None
ALL_PRESENTATION_ASSETS_INTERFACES = None
ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING = None

logger = __import__('logging').getLogger(__name__)


def interface_of_asset(item):
    for iface in ALL_PRESENTATION_ASSETS_INTERFACES:
        if iface.providedBy(item):
            return iface
    if IPresentationAsset.providedBy(item):
        return find_most_derived_interface(item, IPresentationAsset)
    return None
iface_of_asset = interface_of_asset


def _set_ifaces():
    global MARKER_INTERFACES
    global ALL_PRESENTATION_MIME_TYPES
    global COURSE_CONTAINER_INTERFACES
    global PACKAGE_CONTAINER_INTERFACES
    global GROUP_OVERVIEWABLE_INTERFACES
    global ALL_PRESENTATION_ASSETS_INTERFACES

    MARKER_INTERFACES = set()
    ALL_PRESENTATION_MIME_TYPES = set()
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

    MARKER_INTERFACES.update(NO_IMPL_REF_IFACES)

    def _package_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, IPackagePresentationAsset)
                      and item != IPackagePresentationAsset
                      and item not in (INTIMedia, INTIDocketAsset, IConcreteAsset))
        return result
    MARKER_INTERFACES.add(IConcreteAsset)
    MARKER_INTERFACES.add(INTIDocketAsset)
    MARKER_INTERFACES.add(IPackagePresentationAsset)
    
    def _course_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, ICoursePresentationAsset)
                      and item != ICoursePresentationAsset
                      and item not in NO_IMPL_REF_IFACES)
        return result
    MARKER_INTERFACES.add(ICoursePresentationAsset)
     
    def _overview_item_predicate(item):
        result = bool(type(item) == interface.interface.InterfaceClass
                      and issubclass(item, IGroupOverViewable)
                      and item != IGroupOverViewable
                      and item not in NO_IMPL_REF_IFACES)
        return result
    MARKER_INTERFACES.add(IGroupOverViewable)

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
    MARKER_INTERFACES.add(IUserCreatedAsset)
    MARKER_INTERFACES.add(IPresentationAsset)
    MARKER_INTERFACES.add(ILegacyPresentationAsset)
    MARKER_INTERFACES.add(IContentBackedPresentationAsset)
     
    for _, item in inspect.getmembers(module, _course_item_predicate):
        COURSE_CONTAINER_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _package_item_predicate):
        PACKAGE_CONTAINER_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _overview_item_predicate):
        GROUP_OVERVIEWABLE_INTERFACES.add(item)

    for _, item in inspect.getmembers(module, _presentationasset_item_predicate):
        ALL_PRESENTATION_ASSETS_INTERFACES.add(item)

    MARKER_INTERFACES = tuple(MARKER_INTERFACES)
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

    module = sys.modules[__name__]
    for name, item in inspect.getmembers(module, _tuples_item_predicate):
        if name.endswith('MIME_TYPES'):
            ALL_PRESENTATION_MIME_TYPES.update(str(x) for x in item)
    ALL_PRESENTATION_MIME_TYPES = tuple(sorted(ALL_PRESENTATION_MIME_TYPES))


_set_ifaces()
del _set_ifaces


# registration


def register_asset_interface(provided, mimeType):
    global ALL_PRESENTATION_MIME_TYPES
    global COURSE_CONTAINER_INTERFACES
    global PACKAGE_CONTAINER_INTERFACES
    global GROUP_OVERVIEWABLE_INTERFACES
    global ALL_PRESENTATION_ASSETS_INTERFACES
    
    if not mimeType:
        raise ValueError('Must provided a MimeType')
    if mimeType in ALL_PRESENTATION_MIME_TYPES:
        raise ValueError('MimeType has already been registered')
    if not provided.isOrExtends(IPresentationAsset):
        raise TypeError('Not a valid interface')
    if provided in MARKER_INTERFACES:
        raise ValueError('Cannot register a marker interface')

    ALL_PRESENTATION_MIME_TYPES += (mimeType,)
    ALL_PRESENTATION_ASSETS_INTERFACES += (provided,)
    
    if provided.isOrExtends(ICoursePresentationAsset):
        COURSE_CONTAINER_INTERFACES += (provided,)
    if provided.isOrExtends(IPackagePresentationAsset):
        PACKAGE_CONTAINER_INTERFACES += (provided,)
    if provided.isOrExtends(IGroupOverViewable):
        GROUP_OVERVIEWABLE_INTERFACES += (provided,)


# make sure all constants have been loaded
from nti.contenttypes.presentation._patch import patch
patch()
del patch


def asset_iface_with_mimetype(mimetype):
    return ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING.get(mimetype, None)


# mimetype -> iface mapping
def _set_mimetypes_ifaces_mapping():
    global ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING
    if ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING is None:
        ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING = dict()
    for iface in ALL_PRESENTATION_ASSETS_INTERFACES or ():
        mimetype = iface.getTaggedValue('_ext_mime_type')
        ALL_PRESENTATION_ASSETS_MIMETYPES_INTERFACES_MAPPING[mimetype] = iface

_set_mimetypes_ifaces_mapping()
del _set_mimetypes_ifaces_mapping
