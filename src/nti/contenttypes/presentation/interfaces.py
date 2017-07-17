#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from copy import copy

from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable

from zope.container.constraints import contains

from zope.dublincore.interfaces import IDCDescriptiveProperties

from zope.interface.common.mapping import IMapping
from zope.interface.common.sequence import IFiniteSequence

from zope.interface.interfaces import ObjectEvent
from zope.interface.interfaces import IObjectEvent

from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zope.location.interfaces import IContained

from zope.schema import vocabulary

from nti.base.interfaces import IFile
from nti.base.interfaces import ITitled
from nti.base.interfaces import ICreated
from nti.base.interfaces import IIterable
from nti.base.interfaces import ILastModified

from nti.contenttypes.presentation.schema import VisibilityField

from nti.contenttypes.reports.interfaces import IReportContext

from nti.coremetadata.interfaces import IObjectJsonSchemaMaker

from nti.namedfile.interfaces import IFileConstrained

from nti.ntiids.schema import ValidNTIID

from nti.property.property import alias

from nti.publishing.interfaces import ICalendarPublishable

from nti.recorder.interfaces import IRecordable
from nti.recorder.interfaces import IRecordableContainer

from nti.schema.field import Int
from nti.schema.field import Bool
from nti.schema.field import Choice
from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import Variant
from nti.schema.field import Iterable
from nti.schema.field import ValidURI
from nti.schema.field import ValidText
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable
from nti.schema.jsonschema import TAG_HIDDEN_IN_UI
from nti.schema.jsonschema import TAG_REQUIRED_IN_UI

# Transcript types (file extensions)

SBV_TRANSCRIPT_TYPE = u'sbv'
SRT_TRANSCRIPT_TYPE = u'srt'
VTT_TRANSCRIPT_TYPE = u'vtt'
TRANSCRIPT_TYPES = (
    SBV_TRANSCRIPT_TYPE, SRT_TRANSCRIPT_TYPE, VTT_TRANSCRIPT_TYPE)

TRANSCRIPT_TYPE_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in TRANSCRIPT_TYPES])

# Transcript MimeTypes

SBV_TRANSCRIPT_MIMETYPE = u'text/sbv'
SRT_TRANSCRIPT_MIMETYPE = u'text/srt'
VTT_TRANSCRIPT_MIMETYPE = u'text/vtt'
TRANSCRIPT_MIMETYPES = (SBV_TRANSCRIPT_MIMETYPE, SRT_TRANSCRIPT_MIMETYPE,
                        VTT_TRANSCRIPT_MIMETYPE)

TRANSCRIPT_MIMETYPE_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in TRANSCRIPT_MIMETYPES])

# Video Services

HTML5_VIDEO_SERVICE = u'html5'
VIMEO_VIDEO_SERVICE = u'vimeo'
YOUTUBE_VIDEO_SERVICE = u'youtube'
KALTURA_VIDEO_SERVICE = u'kaltura'
VIDEO_SERVICES = (HTML5_VIDEO_SERVICE, VIMEO_VIDEO_SERVICE, YOUTUBE_VIDEO_SERVICE,
                  KALTURA_VIDEO_SERVICE)

VIDEO_SERVICES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in VIDEO_SERVICES])

# Video Service Types

MP4_VIDEO_SERVICE_TYPE = u'video/mp4'
WEBM_VIDEO_SERVICE_TYPE = u'video/webm'
VIMEO_VIDEO_SERVICE_TYPE = u'video/vimeo'
YOUTUBE_VIDEO_SERVICE_TYPE = u'video/youtube'
KALTURA_VIDEO_SERVICE_TYPE = u'video/kaltura'

VIDEO_SERVICE_TYPES = (MP4_VIDEO_SERVICE_TYPE, WEBM_VIDEO_SERVICE_TYPE,
                       YOUTUBE_VIDEO_SERVICE_TYPE, VIMEO_VIDEO_SERVICE_TYPE,
                       KALTURA_VIDEO_SERVICE_TYPE)

VIDEO_SERVICE_TYPES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in VIDEO_SERVICE_TYPES])

# Video Service Sources

MP4_VIDEO_SOURCE = u'mp4'
WEBM_VIDEO_SOURCE = u'webm'
OTHER_VIDEO_SOURCE = u'other'
VIDEO_SOURCES = (MP4_VIDEO_SOURCE, WEBM_VIDEO_SOURCE, OTHER_VIDEO_SOURCE)

VIDEO_SOURCES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in VIDEO_SOURCES])

# Audio Services

HTML5_AUDIO_SERVICE = u'html5'
AUDIO_SERVICES = (HTML5_AUDIO_SERVICE,)

AUDIO_SERVICES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in AUDIO_SERVICES])

# Audio Service Types

MP3_AUDIO_SERVICE_TYPE = u'audio/mp3'
WAV_AUDIO_SERVICE_TYPE = u'audio/wav'

AUDIO_SERVICE_TYPES = (MP3_AUDIO_SERVICE_TYPE, WAV_AUDIO_SERVICE_TYPE)

AUDIO_SERVICE_TYPES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in AUDIO_SERVICE_TYPES])

# Audio Service Sources

MP3_AUDIO_SOURCE = u'mp4'
WAV_AUDIO_SOURCE = u'webm'
OTHER_AUDIO_SOURCE = u'other'
AUDIO_SOURCES = (MP3_AUDIO_SOURCE, WAV_AUDIO_SOURCE, OTHER_AUDIO_SOURCE)

AUDIO_SOURCES_VOCABULARY = \
    vocabulary.SimpleVocabulary(
        [vocabulary.SimpleTerm(x) for x in AUDIO_SOURCES])

#: OU Visibility
OU = u"OU"

#: Public Visibility
PUBLIC = u'Public'

#: Credit Visibility
CREDIT = u"ForCredit"

#: Everyone Visibility
EVERYONE = u'everyone'

#: Purchased Visibility
PURCHASED = u"Purchased"


def byline_schema_field(required=False):
    return Variant((ValidTextLine(title=u"Creator name"),
                    Object(interface.Interface, title=u"Creator object")),
                   required=required)


def href_schema_field(title=u'', required=False, default=None):
    return Variant((ValidTextLine(title=u"href name"),
                    ValidURI(title=u"href source uri"),
                    Object(IFile, title=u"href file")),
                   title=title,
                   default=default,
                   required=required)


class ITaggedContent(interface.Interface):
    """
    Something that can contain tags.
    """

    tags = IndexedIterable(title=u"Tags applied by the user.",
                           value_type=ValidTextLine(min_length=1,
                                                    title=u"A single tag"),
                           unique=True,
                           default=(),
                           required=False)


class IPresentationAsset(ILastModified, IContained, IAttributeAnnotatable):
    """
    marker interface for all presentation assests
    """
IPresentationAsset.setTaggedValue('_ext_jsonschema', u'')


class IConcreteAsset(IPresentationAsset, IRecordable):
    """
    Marker interface for non-ref (concrete) types
    """
IConcreteAsset.setTaggedValue('_ext_is_marker_interface', True)


class IUserCreatedAsset(interface.Interface):
    """
    Marker interface for user created asset
    """
IUserCreatedAsset.setTaggedValue('_ext_is_marker_interface', True)


class IPackagePresentationAsset(IPresentationAsset):
    """
    Marker interface for assets whose home are content packages
    """
IPackagePresentationAsset.setTaggedValue('_ext_is_marker_interface', True)


class ICoursePresentationAsset(IPresentationAsset):
    """
    Marker interface for assets whose home are courses
    """
ICoursePresentationAsset.setTaggedValue('_ext_is_marker_interface', True)


class ILegacyPresentationAsset(IPresentationAsset):
    """
    Marker interface for assets that come from legacy courses/packages
    """
ILegacyPresentationAsset.setTaggedValue('_ext_is_marker_interface', True)


class IContentBackedPresentationAsset(interface.Interface):
    """
    Marker interface for assets that come from content backed sources
    """
IContentBackedPresentationAsset.setTaggedValue(
    '_ext_is_marker_interface', True)


class IPointer(interface.Interface):
    """
    Marker interface for objects that point to another
    """
    target = interface.Attribute("target object id")
IPointer.setTaggedValue('_ext_is_marker_interface', True)


class IAssetRef(IPresentationAsset, IPointer):
    """
    Marker interface for pointer-presentation assets
    """
IAssetRef.setTaggedValue('_ext_is_marker_interface', True)


class IItemAssetContainer(interface.Interface):
    """
    Base interface for assets that containt other assets
    """

    Items = interface.Attribute("Items in this container")

    def append(item):
        """
        Add an item
        """

    def remove(item):
        """
        remove the specified item

        :return True if object was removed
        """

    def __contains__(item):
        """
        return is the specified item is in this container
        """


class IGroupOverViewable(interface.Interface):
    """
    marker interface for things that can be part of a course overview group
    """
IGroupOverViewable.setTaggedValue('_ext_is_marker_interface', True)


class IUserCreatedTranscript(interface.Interface):
    """
    Marker interface for user created transcript
    """
IUserCreatedTranscript.setTaggedValue('_ext_is_marker_interface', True)


class INTITranscript(ILastModified, IContained):

    src = href_schema_field(title=u"Transcript source",
                            required=False)

    srcjsonp = href_schema_field(title=u"Transcript source jsonp",
                                 required=False)

    lang = ValidTextLine(title=u"Transcript language",
                         required=True,
                         default=u'en')

    type = Choice(vocabulary=TRANSCRIPT_MIMETYPE_VOCABULARY,
                  title=u'Transcript mimetype',
                  required=True,
                  default=VTT_TRANSCRIPT_MIMETYPE)

    purpose = ValidTextLine(title=u"Transcript purpose",
                            required=True,
                            default=u'normal')

    def is_source_attached(self):
        """
        returns true if the transcript source is attached to this object
        """


class INTIIDIdentifiable(interface.Interface):

    ntiid = ValidNTIID(title=u"Item NTIID", required=False, default=None)


class INTIMediaSource(ILastModified, IContained):

    service = ValidTextLine(title=u"Source service", required=True)

    thumbnail = href_schema_field(title=u"Source thumbnail", required=False)


class IVisibilityOptionsProvider(interface.Interface):
    """
    Utility for an asset visibility options
    """

    def iter_options(self):
        """
        Return an iterable of visibility options
        """


class IVisible(interface.Interface):
    """
    marker interface for things that have visibility
    """
    visibility = VisibilityField(title=u'Media ref visibility',
                                 required=False)


class INTIMediaRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
                   ICoursePresentationAsset, IVisible, IRecordable):
    target = ValidNTIID(title=u"Target NTIID", required=False)
IMediaRef = INTIMediaRef  # BWC


class IAssetTitled(interface.Interface):
    title = ValidTextLine(title=u"Asset title", required=False)


class IAssetTitleDescribed(IAssetTitled, IDCDescriptiveProperties):
    # IDCDescriptiveProperties marker needed for ext adapter.
    title = copy(IAssetTitled['title'])
    title.default = u''

    description = ValidTextLine(title=u"Media description",
                                required=False,
                                default=u'')


class INTIMedia(IAssetTitleDescribed, INTIIDIdentifiable,
                ICreated, IPackagePresentationAsset,
                IRecordable, IFileConstrained):

    byline = byline_schema_field(required=False)


class ITranscriptContainer(IFiniteSequence):

    def clear():
        """
        clear all transcripts
        """

    def add(transcript):
        """
        add a :class: `INTITranscript` object
        """

    def remove(transcript):
        """
        remove a :class: `INTITranscript` object
        """

    def __iter__():
        pass


class INTIVideoSource(INTIMediaSource):

    width = Int(title=u"Video width", required=False)

    height = Int(title=u"Video height", required=False)

    poster = ValidTextLine(title=u"Video poster", required=False)

    service = Choice(vocabulary=VIDEO_SERVICES_VOCABULARY,
                     title=u'Video service',
                     required=True,
                     default=HTML5_VIDEO_SERVICE)

    source = IndexedIterable(Variant((Choice(vocabulary=VIDEO_SOURCES_VOCABULARY),
                                      ValidTextLine())),
                             title=u'Video source',
                             required=True,
                             min_length=1)

    type = IndexedIterable(Choice(vocabulary=VIDEO_SERVICE_TYPES_VOCABULARY),
                           title=u'Video service types',
                           required=True,
                           min_length=1)
INTIVideoSource.setTaggedValue('_ext_jsonschema', u'videosource')


class INTIVideo(INTIMedia):

    subtitle = Bool(title=u"Subtitle flag", required=False, default=None)

    closed_caption = Bool(title=u"Close caption flag",
                          required=False,
                          default=None)

    sources = IndexedIterable(value_type=Object(INTIVideoSource),
                              title=u"The video sources",
                              required=False,
                              min_length=0)

    transcripts = IndexedIterable(value_type=Object(INTITranscript),
                                  title=u"The transcripts",
                                  required=False,
                                  min_length=0)

INTIVideo.setTaggedValue('_ext_jsonschema', u'video')

INTIVideo['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideo['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIVideo['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideo['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIVideoRef(INTIMediaRef):

    label = ValidText(title=u"Video label", required=False)

    poster = ValidTextLine(title=u"Video poster", required=False)

INTIVideoRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideoRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIAudioSource(INTIMediaSource):

    service = Choice(vocabulary=AUDIO_SERVICES_VOCABULARY,
                     title=u'Audio service',
                     required=True,
                     default=HTML5_AUDIO_SERVICE)

    source = IndexedIterable(Variant((Choice(vocabulary=AUDIO_SOURCES_VOCABULARY),
                                      ValidTextLine())),
                             title=u'Audio source',
                             required=True,
                             min_length=1)

    type = IndexedIterable(Choice(vocabulary=AUDIO_SERVICE_TYPES_VOCABULARY),
                           title=u'Audio service types',
                           required=True,
                           min_length=1)

INTIAudioSource.setTaggedValue('_ext_jsonschema', u'audiosource')


class INTIAudio(INTIMedia):

    sources = IndexedIterable(value_type=Object(INTIAudioSource),
                              title=u"The audio sources",
                              required=False,
                              min_length=1)

    transcripts = IndexedIterable(value_type=Object(INTITranscript),
                                  title=u"The transcripts",
                                  required=False,
                                  min_length=0)


INTIAudio.setTaggedValue('_ext_jsonschema', u'audio')

INTIAudio['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAudio['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIAudio['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAudio['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIAudioRef(INTIMediaRef):
    pass


class INTIMediaRoll(IItemAssetContainer, IGroupOverViewable, INTIIDIdentifiable,
                    ICreated, ICoursePresentationAsset, IIterable, IConcreteAsset,
                    IFiniteSequence, IRecordable):

    Items = IndexedIterable(value_type=Object(INTIMediaRef),
                            title=u"The media sources",
                            required=False, min_length=0)

    def pop(idx):
        """
        remove the item at the specified index
        """

INTIMediaRoll.setTaggedValue('_ext_jsonschema', u'mediaroll')


class INTIAudioRoll(INTIMediaRoll):

    Items = IndexedIterable(value_type=Object(INTIAudioRef),
                            title=u"The audio sources",
                            required=False,
                            min_length=0)

INTIAudioRoll.setTaggedValue('_ext_jsonschema', u'audioroll')


class INTIVideoRoll(INTIMediaRoll):

    Items = IndexedIterable(value_type=Object(INTIVideoRef),
                            title=u"The audio sources",
                            required=False,
                            min_length=0)

INTIVideoRoll.setTaggedValue('_ext_jsonschema', u'videoroll')


class INTISlide(INTIIDIdentifiable, IPackagePresentationAsset, IRecordable):

    slidevideoid = ValidNTIID(title=u"Slide video NTIID", required=True)

    slidedeckid = ValidNTIID(title=u"Slide deck NTIID", required=False)

    slidevideostart = Number(title=u"Video start", required=False, default=0)

    slidevideoend = Number(title=u"Video end", required=False, default=0)

    slideimage = href_schema_field(title=u"Slide image source", required=False)

    slidenumber = Int(title=u"Slide number", required=True, default=1)


class INTISlideVideo(IAssetTitleDescribed, INTIIDIdentifiable,
                     ICreated, IPackagePresentationAsset, IRecordable):

    byline = byline_schema_field(required=False)

    video_ntiid = ValidNTIID(title=u"Slide video NTIID", required=True)

    slidedeckid = ValidNTIID(title=u"Slide deck NTIID", required=False)

    thumbnail = href_schema_field(title=u"Slide video thumbnail",
                                  required=False)

INTISlideVideo['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideVideo['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTISlideVideo['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideVideo['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTISlideDeck(IItemAssetContainer, INTIMedia):

    Slides = IndexedIterable(value_type=Object(INTISlide),
                             title=u"The slides",
                             required=False,
                             min_length=1)

    Videos = IndexedIterable(value_type=Object(INTISlideVideo),
                             title=u"The slide videos",
                             required=False,
                             min_length=1)

    slidedeckid = ValidNTIID(title=u"Slide deck NTIID", required=False)

    byline = byline_schema_field(required=False)

    Items = Iterable(title=u'All items in the slide deck',
                     readonly=True,
                     required=False)
    Items.setTaggedValue('_ext_excluded_out', True)

INTISlideDeck.setTaggedValue('_ext_jsonschema', u'slidedeck')

INTISlideDeck['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideDeck['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTISlideDeck['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideDeck['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTISlideDeckRef(INTIMediaRef):
    target = ValidNTIID(title=u"Target NTIID", required=False)
ISlideDeckRef = INTISlideDeckRef  # BWC


class INTITimelineRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
                      ICoursePresentationAsset):
    target = ValidNTIID(title=u"Target NTIID", required=False)
ITimelineRef = INTITimelineRef  # BWC


class INTIRelatedWorkRefPointer(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
                                ICoursePresentationAsset):
    target = ValidNTIID(title=u"Target NTIID", required=False)


class INTIDocketAsset(IPackagePresentationAsset, INTIIDIdentifiable,
                      IGroupOverViewable, IPointer):

    label = ValidTextLine(title=u"The label", required=True, default=u'')

    href = href_schema_field(title=u"Resource href",
                             required=False,
                             default=u'')

    icon = href_schema_field(title=u"Icon href", required=False)

    target = ValidNTIID(title=u"Target NTIID", required=False)
INTIDocketMixin = INTIDocketAsset  # BWC


class INTITimeline(INTIDocketAsset, IGroupOverViewable,
                   IRecordable, IFileConstrained):
    description = ValidTextLine(title=u"Timeline description", required=False)

    suggested_inline = Bool(u"Suggested inline flag",
                            required=False,
                            default=False)

INTITimeline['href'].setTaggedValue(TAG_REQUIRED_IN_UI, True)


class INTIRelatedWorkRef(INTIDocketAsset, ICreated, IVisible,
                         IRecordable, IFileConstrained):
    byline = byline_schema_field(required=False)

    section = ValidTextLine(title=u"Section", required=False)

    description = ValidText(title=u"Slide video description", required=False)

    type = ValidTextLine(title=u"The target mimetype", required=False)

    ntiid = Variant((ValidTextLine(title=u"Related content ntiid"),
                     ValidNTIID(title=u"Related content ntiid")),
                    required=False,
                    default=None)

    nti_requirements = ValidTextLine(title=u"NTI requirements", required=False)

    target = ValidTextLine(title=u"Related work target", required=False)


class INTIDiscussionRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
                        ITitled, ICoursePresentationAsset,
                        IRecordable, IFileConstrained):
    title = ValidTextLine(title=u"Discussion title", required=False)

    icon = href_schema_field(title=u"Discussion icon href", required=False)

    label = ValidTextLine(title=u"The label", required=False, default=u'')

    ntiid = Variant((ValidTextLine(title=u"Discussion NTIID"),
                     ValidNTIID(title=u"Discussion NTIID")),
                    required=False,
                    default=None)

    target = Variant((ValidTextLine(title=u"Target NTIID"),
                      ValidNTIID(title=u"Target NTIID")),
                     required=False)

    id = ValidTextLine(title=u"Discussion identifier", required=True)
    id.setTaggedValue('__external_accept_id__', True)

    def isCourseBundle():
        """
        return if this DiscussionRef refers to a course bundle
        """
    is_course_bundle = isCourseBundle

INTIDiscussionRef['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIDiscussionRef['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIDiscussionRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIDiscussionRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIAssessmentRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
                        ICoursePresentationAsset):
    target = ValidNTIID(title=u"Target NTIID", required=True)

    label = ValidTextLine(title=u"The label", required=False, default=u'')
IAssessmentRef = INTIAssessmentRef  # BWC

INTIAssessmentRef['target'].setTaggedValue(TAG_REQUIRED_IN_UI, True)


class INTIQuestionSetRef(INTIAssessmentRef):
    question_count = Int(title=u"Question count", required=False)
IQuestionSetRef = INTIQuestionSetRef  # BWC

INTIQuestionSetRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIQuestionSetRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIQuestionRef(INTIAssessmentRef):
    pass
IQuestionRef = INTIQuestionRef  # BWC

INTIQuestionRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIQuestionRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIAssignmentRef(INTIAssessmentRef, IAssetTitled):
    containerId = ValidNTIID(title=u"Container NTIID", required=False)
IAssignmentRef = INTIAssignment = INTIAssignmentRef  # BWC

INTIAssignmentRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAssignmentRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIAssignmentRef['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAssignmentRef['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTIInquiryRef(INTIAssessmentRef, IReportContext):
    pass


class INTIPollRef(INTIInquiryRef):
    pass
IPollRef = INTIPollRef  # BWC

INTIPollRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIPollRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTISurveyRef(INTIInquiryRef):

    containerId = ValidNTIID(title=u"Container NTIID", required=False)

    question_count = Int(title=u"Question count", required=False)
ISurveyRef = INTISurveyRef  # BWC

INTISurveyRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISurveyRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTICourseOverviewSpacer(IGroupOverViewable, INTIIDIdentifiable,
                               ICoursePresentationAsset):
    pass


class INTICourseOverviewGroup(IItemAssetContainer, IAssetTitled, INTIIDIdentifiable,
                              ICoursePresentationAsset, IFiniteSequence, IIterable,
                              IRecordableContainer, IConcreteAsset):

    Items = IndexedIterable(value_type=Object(IGroupOverViewable),
                            title=u"The overview items",
                            required=False,
                            min_length=0)

    accentColor = ValidTextLine(title=u"Overview color", required=False)

INTICourseOverviewGroup.setTaggedValue('_ext_jsonschema', u'overviewgroup')

INTICourseOverviewGroup['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTICourseOverviewGroup['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTICourseOverviewGroup['accentColor'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTICourseOverviewGroup['accentColor'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class INTILessonOverview(IItemAssetContainer, IAssetTitled, INTIIDIdentifiable,
                         ICoursePresentationAsset, IFiniteSequence, IIterable,
                         IRecordableContainer, ICalendarPublishable, IConcreteAsset):

    Items = IndexedIterable(value_type=Object(INTICourseOverviewGroup),
                            title=u"The overview items",
                            required=False,
                            min_length=0)
    lesson = ValidTextLine(title=u"Lesson NTIID", required=False)

    def pop(idx):
        """
        remove the group at the specified index
        """

INTILessonOverview.setTaggedValue('_ext_jsonschema', u'lesson')

INTILessonOverview['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTILessonOverview['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)


class ILessonPublicationConstraints(IMapping,
                                    ICreated,
                                    ILastModified):
    """
    Defines a container for lesson publication constraints
    """

    contains('.ILessonPublicationConstraint')
    __setitem__.__doc__ = None

    Items = IndexedIterable(title=u"The contained constraint items",
                            readonly=True)
    Items.setTaggedValue('_ext_excluded_out', True)

    def append(constraint):
        """
        Add the specified contraint to this container
        """

    def extend(constraints):
        """
        Add the specified contraints to this container
        """

    def clear():
        """
        Remove all contraints
        """


class ILessonPublicationConstraint(ICreated, ILastModified):
    """
    Defines a constraint for determining whether a lesson
    is publishable or not
    """


class IAssignmentCompletionConstraint(ILessonPublicationConstraint):
    """
    A publication constraint that is satisfied if all its
    referenced assignments are either completed or closed.
    """
    assignments = IndexedIterable(title=u"Assignments NTIIDs.",
                                  value_type=ValidNTIID(min_length=1,
                                                        title=u"A single NTIID"),
                                  unique=True,
                                  required=True,
                                  min_length=1)


class ISurveyCompletionConstraint(ILessonPublicationConstraint):
    """
    A publication constraint that is satisfied if all its
    referenced surveys are either completed or closed.
    """
    surveys = IndexedIterable(title=u'Survey NTIIDs',
                              value_type=ValidNTIID(min_length=1,
                                                    title=u'A single NTIID'),
                              unique=True,
                              required=True,
                              min_length=1)


class ILessonPublicationConstraintChecker(interface.Interface):

    def is_satisfied(constraint, principal=None):
        """
        Return whether or not a constraint is satisfied.
        """

    def satisfied_time(user):
        """
        Return the time when a constraint is satisfied,
        0 if it is not applicable (for instructors or editors),
        or None if the constraint has not been satisfied.
        """

    def get_constraint_items(self):
        """
        Returns a list of items that need to be satisfied for 
        this constraint to be considered satisfied.
        """

    def check_time_constraint_item(self, item_ntiid, histories):
        """
        Return the time when a constraint item is satisfied or 
        None if it has not been satisfied. This should be
        implemented for each type of constraint.
        """


class IPresentationVisibility(interface.Interface):
    """
    marker interface to return the visibility for an object.

    Register as an adapter
    """

    def visibility():
        pass


class IPresentationAssetContainer(IMapping):
    """
    Something that is an unordered bag of presentation asset items

    This package provides no implementation of this interface. (But
    something like the content library package may be adaptable to this,
    typically with annotations).
    """

    def append(item):
        """
        Add an item to this container
        """

    def extend(items):
        """
        Add the specified items to this container
        """

    def assets():
        """
        return an iterable with all assets this container
        """

    def pop(k, *args):
        """
        remove specified key and return the corresponding value
        *args may contain a single default value, or may not be supplied.
        If key is not found, default is returned if given, otherwise
        KeyError is raised
        """


class IPresentationAssetAffiliations(interface.Interface):
    """
    subscriber for a presentation asset containers
    """

    def containers(item):
        """
        return the containers that refer to specified item
        """


class IPresentationAssetJsonSchemaMaker(IObjectJsonSchemaMaker):
    """
    Marker interface for a presentation asset Json Schema maker utility
    """

    def make_schema(schema=IPresentationAsset, user=None):
        pass


class IPresentationAssetCreatedEvent(IObjectCreatedEvent):
    principal = interface.Attribute("Creator principal")

    externalValue = interface.Attribute("External object")


@interface.implementer(IPresentationAssetCreatedEvent)
class PresentationAssetCreatedEvent(ObjectCreatedEvent):

    def __init__(self, obj, principal=None, externalValue=None):
        super(PresentationAssetCreatedEvent, self).__init__(obj)
        self.principal = principal
        self.externalValue = externalValue


class IWillUpdatePresentationAssetEvent(IObjectEvent):
    principal = interface.Attribute("Updater principal")
    externalValue = interface.Attribute("External object")


@interface.implementer(IWillUpdatePresentationAssetEvent)
class WillUpdatePresentationAssetEvent(ObjectEvent):

    def __init__(self, obj, principal=None, externalValue=None):
        super(WillUpdatePresentationAssetEvent, self).__init__(obj)
        self.principal = principal
        self.externalValue = externalValue


class IWillRemovePresentationAssetEvent(IObjectEvent):
    pass


@interface.implementer(IWillRemovePresentationAssetEvent)
class WillRemovePresentationAssetEvent(ObjectEvent):
    pass


#: Asset removed from item asset container
TRX_ASSET_REMOVED_FROM_ITEM_ASSET_CONTAINER = u'assetremovedfromitemcontainer'


class IItemRemovedFromItemAssetContainerEvent(IObjectModifiedEvent):
    pass


@interface.implementer(IItemRemovedFromItemAssetContainerEvent)
class ItemRemovedFromItemAssetContainerEvent(ObjectModifiedEvent):
    pass


#: Overview group moved recorder transaction type.
TRX_OVERVIEW_GROUP_MOVE_TYPE = u'overviewgroupmoved'


class IOverviewGroupMovedEvent(IObjectEvent):
    pass


@interface.implementer(IOverviewGroupMovedEvent)
class OverviewGroupMovedEvent(ObjectEvent):

    group = alias('object')

    def __init__(self, obj, principal=None, index=None, old_parent_ntiid=None):
        super(OverviewGroupMovedEvent, self).__init__(obj)
        self.index = index
        self.principal = principal
        self.old_parent_ntiid = old_parent_ntiid


#: Asset moved recorder transaction type.
TRX_ASSET_MOVE_TYPE = u'presentationassetmoved'


class IPresentationAssetMovedEvent(IObjectEvent):
    pass


@interface.implementer(IPresentationAssetMovedEvent)
class PresentationAssetMovedEvent(ObjectEvent):

    asset = alias('object')

    def __init__(self, obj, principal=None, index=None, old_parent_ntiid=None):
        super(PresentationAssetMovedEvent, self).__init__(obj)
        self.index = index
        self.principal = principal
        self.old_parent_ntiid = old_parent_ntiid


import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    "Import from INTIRelatedWorkRef instead",
    INTIRelatedWork='nti.contenttypes.presentation.interfaces:INTIRelatedWorkRef')


# catalog


class ISiteAdapter(interface.Interface):
    """
    Adapts contained objects to their site.
    """
    site = interface.Attribute("site string")


class IContainedTypeAdapter(interface.Interface):
    """
    Adapts contained objects to their str type.
    """
    type = interface.Attribute("type string")


class INamespaceAdapter(interface.Interface):
    """
    Adapts contained objects to their str namespace.
    """
    namespace = interface.Attribute("namespace string")


class INTIIDAdapter(interface.Interface):
    """
    Adapts contained objects to their str NTIID.
    """
    ntiid = interface.Attribute("NTIID string")


class IContainersAdapter(interface.Interface):
    """
    Adapts contained objects to their str containers NTIIDs.
    """
    containers = interface.Attribute("NTIID strings")


class ISlideDeckAdapter(interface.Interface):
    """
    Adapts contained objects to their video NTIIDs
    """
    videos = interface.Attribute("NTIID strings")


class ITargetAdapter(interface.Interface):
    """
    Adapts contained objects to their target type.
    """
    target = interface.Attribute("NTIID string")


class IUserAssetVisibilityUtility(interface.Interface):
    """
    Determines if the user has access to the given asset and
    course context.
    """

    def is_item_visible(self, item, user=None, course=None):
        """
        :return: a bool if the item is visible to the user.
        """
