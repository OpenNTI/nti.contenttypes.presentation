#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
import copy
import zlib
import base64
from collections import Mapping
from collections import MutableSequence

from zope import component
from zope import interface

from persistent.list import PersistentList

from nti.base.interfaces import DEFAULT_CONTENT_TYPE

from nti.contenttypes.presentation import TIMELINE
from nti.contenttypes.presentation import RELATED_WORK
from nti.contenttypes.presentation import JSON_TIMELINE
from nti.contenttypes.presentation import RELATED_WORK_REF
from nti.contenttypes.presentation import TEXT_VTT_MIMETYPE
from nti.contenttypes.presentation import TIMELINE_MIME_TYPES
from nti.contenttypes.presentation import NTI_LESSON_OVERVIEW
from nti.contenttypes.presentation import SLIDE_DECK_MIME_TYPES
from nti.contenttypes.presentation import NTI_TRANSCRIPT_MIMETYPE
from nti.contenttypes.presentation import TIMELINE_REF_MIME_TYPES
from nti.contenttypes.presentation import SLIDE_DECK_REF_MIME_TYPES
from nti.contenttypes.presentation import ALL_MEDIA_ROLL_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_POINTER_MIME_TYPES

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
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIQuestionRef
from nti.contenttypes.presentation.interfaces import INTITimelineRef
from nti.contenttypes.presentation.interfaces import INTISlideDeckRef
from nti.contenttypes.presentation.interfaces import INTIAssignmentRef
from nti.contenttypes.presentation.interfaces import INTIDiscussionRef
from nti.contenttypes.presentation.interfaces import INTIQuestionSetRef
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef
from nti.contenttypes.presentation.interfaces import IUserCreatedTranscript
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTICourseOverviewSpacer
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRefPointer
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraints
from nti.contenttypes.presentation.interfaces import IContentBackedPresentationAsset

from nti.contenttypes.presentation.media import NTITranscriptFile

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

logger = __import__('logging').getLogger(__name__)


# assets


def ntiid_check(s):
    s = s.strip() if s else s
    s = s[1:] if s and (s.startswith('"') or s.startswith("'")) else s
    s = s[6:] if s and s.startswith("relwk:tag:") else s
    return s


def parse_embedded_transcript(transcript, parsed, encoded=True):
    contents = parsed['contents']
    filename = parsed.pop('filename', None) or "transcript.vtt"
    # parse content type
    contentType = parsed.get('contentType') or parsed.get('type')
    contentType = contentType or TEXT_VTT_MIMETYPE
    if contentType == DEFAULT_CONTENT_TYPE:
        contentType = TEXT_VTT_MIMETYPE
    # handle content
    if encoded:
        contents = base64.b64decode(contents)
        contents = zlib.decompress(contents)
    # create transcript
    result = NTITranscriptFile(contentType)
    result.data = contents
    result.name = result.filename = filename
    result.__parent__ = transcript
    transcript.src = result # set source
    transcript.srcjsonp = None
    interface.alsoProvides(transcript, IUserCreatedTranscript)
    return result


@component.adapter(INTITranscript)
@interface.implementer(IInternalObjectUpdater)
class _NTITranscriptUpdater(InterfaceObjectIO):

    _ext_iface_upper_bound = INTITranscript

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        source = parsed.get('src')
        contents = parsed.get('contents', None)
        result = super(_NTITranscriptUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        if not contents:
            if source and not isinstance(source, six.string_types):
                raise AssertionError("Source is not a string")
        else:
            transcript = self._ext_replacement()
            parse_embedded_transcript(transcript, parsed)
            transcript.srcjsonp = None  # pylint: disable=attribute-defined-outside-init
        return result


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
        return self

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
                transcript[MIMETYPE] = NTI_TRANSCRIPT_MIMETYPE
            obj = find_factory_for(transcript)()
            transcripts[idx] = update_from_external_object(obj, transcript)
        if transcripts:
            transcripts = PersistentList(transcripts or ())
            parsed['transcripts'] = transcripts
        return self

    def fixAll(self, parsed):
        self.fixCreator(parsed).parseTranscripts(parsed)
        return parsed

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        result = super(_NTIMediaUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        self.takeOwnership(self._ext_self,
                           getattr(self._ext_self, 'transcripts', None))
        return result


@component.adapter(INTIVideo)
class _NTIVideoUpdater(_NTIMediaUpdater):

    _ext_iface_upper_bound = INTIVideo

    def parseSources(self, parsed):
        sources = parsed.get('sources')
        for idx, source in enumerate(sources or ()):
            if not isinstance(source, Mapping):
                continue
            if MIMETYPE not in source:
                source[MIMETYPE] = 'application/vnd.nextthought.ntivideosource'
            obj = find_factory_for(source)()
            sources[idx] = update_from_external_object(obj, source)
        return self

    def fixCloseCaption(self, parsed):
        if 'closedCaptions' in parsed:
            parsed['closed_caption'] = parsed['closedCaptions']
        elif 'closedCaption' in parsed:
            parsed['closed_caption'] = parsed['closedCaption']
        return self

    def fixAll(self, parsed):
        self.parseSources(parsed).parseTranscripts(parsed) \
            .fixCloseCaption(parsed).fixCreator(parsed)
        return parsed

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        result = super(_NTIVideoUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        self.takeOwnership(self._ext_self,
                           getattr(self._ext_self, 'sources', None))
        return result


@component.adapter(INTIAudio)
class _NTIAudioUpdater(_NTIMediaUpdater):

    _ext_iface_upper_bound = INTIAudio

    def parseSources(self, parsed):
        sources = parsed.get('sources')
        for idx, source in enumerate(sources or ()):
            if not isinstance(source, Mapping):
                continue
            if MIMETYPE not in source:
                source[MIMETYPE] = 'application/vnd.nextthought.ntiaudiosource'
            obj = find_factory_for(source)()
            sources[idx] = update_from_external_object(obj, source)
        return self

    def fixAll(self, parsed):
        self.fixCreator(parsed).parseSources(parsed).parseTranscripts(parsed)
        return parsed

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        result = super(_NTIAudioUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        self.takeOwnership(self._ext_self,
                           getattr(self._ext_self, 'sources', None))
        return result


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
            parsed['ntiid'] = ntiid_check(parsed[NTIID])
        elif 'ntiid' in parsed:
            parsed['ntiid'] = ntiid_check(parsed['ntiid'])

        target = self.getTargetNTIID(parsed)
        if target:
            parsed['target'] = target

        if transfer:
            ntiid, target = parsed.get('ntiid'), parsed.get('target')
            # Pop ntiid if no target or if it is equal to target (and non null)
            # We do not want the target ntiid to match the NTIID field (leads
            # to all sorts of possible issues). We also do not want to
            # explicitly set target to None.
            if ntiid and (not target or target == ntiid):
                parsed['target'] = ntiid
                parsed.pop('ntiid', None)
                parsed.pop(NTIID, None)
        return self


class _NTIMediaRefUpdater(_TargetNTIIDUpdater):

    def fixTarget(self, parsed, unused_transfer=False):
        return _TargetNTIIDUpdater.fixTarget(self, parsed, True)

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
            parsed['video_ntiid'] = ntiid_check(parsed.pop('video-ntiid'))
        return self.fixCreator(parsed)


@component.adapter(INTISlideDeck)
class _NTISlideDeckUpdater(_AssetUpdater):

    _ext_iface_upper_bound = INTISlideDeck

    def parseSlides(self, parsed):
        if 'Slides' in parsed:
            slides = PersistentList(parsed.get('Slides') or ())
            parsed['Slides'] = slides
        return self

    def parseVideos(self, parsed):
        if 'Videos' in parsed:
            videos = PersistentList(parsed.get('Videos') or ())
            parsed['Videos'] = videos
        return self

    def fixAll(self, parsed):
        self.fixCreator(parsed)

        if 'slidedeckid' in parsed and not parsed.get('ntiid'):
            parsed['ntiid'] = ntiid_check(parsed['slidedeckid'])

        if 'ntiid' in parsed and not parsed.get('slidedeckid'):
            parsed['slidedeckid'] = ntiid_check(parsed['ntiid'])

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
            parsed['ntiid'] = ntiid_check(parsed[NTIID])
        if 'desc' in parsed:
            parsed['description'] = parsed.pop('desc')
        if 'suggested-inline' in parsed:
            parsed['suggested_inline'] = parsed.pop('suggested-inline')
        return self.fixCreator(parsed)


@component.adapter(INTIRelatedWorkRef)
class _NTIRelatedWorkRefUpdater(_TargetNTIIDUpdater):

    _ext_iface_upper_bound = INTIRelatedWorkRef

    def fixTarget(self, parsed, transfer=False):
        return _TargetNTIIDUpdater.fixTarget(self, parsed, transfer=False)

    def fixAll(self, parsed):
        if 'desc' in parsed:
            parsed['description'] = parsed.pop('desc')

        self.fixTarget(parsed)

        if 'targetMimeType' in parsed:
            parsed['type'] = parsed.pop('targetMimeType')

        if      IContentBackedPresentationAsset.providedBy(self._ext_self) \
            and getattr(self._ext_self, 'type', '') == 'application/pdf':
            # Only API created PDF refs can change their uploaded files.
            # Import/export does not handle this case currently for
            # content backed assets.
            self.popTargets(parsed)

        return self.fixCreator(parsed)

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        """
        For content backed assets, we do not want to allow `href` edits
        of relative paths.
        """
        if      self._ext_self.href \
            and self._ext_self.href.startswith('resources/'):
            parsed.pop('href', None)
        return super(_NTIRelatedWorkRefUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)


_NTIRelatedWorkUpdater = _NTIRelatedWorkRefUpdater


@component.adapter(INTIDiscussionRef)
class _NTIDiscussionRefUpdater(_TargetNTIIDUpdater):

    _ext_iface_upper_bound = INTIDiscussionRef
    _excluded_in_ivars_ = frozenset(
        InterfaceObjectIO._excluded_in_ivars_ - {'id'}  # pylint: disable=protected-access
    )

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
            parsed['title'] = parsed['label']
        elif not parsed.get('label') and parsed.get('title'):
            parsed['label'] = parsed['title']
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
            parsed['question_count'] = int(parsed.pop('question-count'))
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
        if not parsed.get('title') and parsed.get('label'):
            parsed['title'] = parsed['label']
        elif not parsed.get('label') and parsed.get('title'):
            parsed['label'] = parsed['title']
        if 'question-count' in parsed:
            parsed['question_count'] = int(parsed.pop('question-count'))
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
            parsed['ntiid'] = ntiid_check(parsed[NTIID])
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
            parsed['ntiid'] = ntiid_check(parsed[NTIID])
        ntiid = parsed.get('ntiid')
        lesson = parsed.get('lesson')
        # make sure we update the incoming ntiid
        # since in legacy it may the ntiid of a content unit
        if      not lesson \
            and is_valid_ntiid_string(ntiid) \
            and get_type(ntiid) != NTI_LESSON_OVERVIEW:
            lesson = make_ntiid(nttype=NTI_LESSON_OVERVIEW, base=ntiid)
            parsed['ntiid'] = lesson
            parsed['lesson'] = ntiid
        # use persistent lists
        if ITEMS in parsed:
            items = PersistentList(parsed.get(ITEMS) or ())
            parsed[ITEMS] = items
        return self.fixCreator(parsed)

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        result = super(_NTILessonOverviewUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        self.takeOwnership(self._ext_self, self._ext_self)
        return result

# pre-hooks

# Need to get rid of pre_hook usage. This should be easy, register
# mimetype factory, for most cases. But we do some other special
# handling too.
# https://github.com/NextThought/nti.externalization/issues/29
def internalization_ntivideo_pre_hook(k, x):
    if isinstance(x, Mapping) and 'mimeType' in x:
        x[MIMETYPE] = x.pop('mimeType')
internalization_ntiaudio_pre_hook = internalization_ntivideo_pre_hook


def internalization_assignmentref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.assessment.assignment":
        x[MIMETYPE] = "application/vnd.nextthought.assignmentref"


def internalization_surveyref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.nasurvey":
        x[MIMETYPE] = "application/vnd.nextthought.surveyref"


def internalization_pollref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.napoll":
        x[MIMETYPE] = "application/vnd.nextthought.pollref"


def internalization_questionsetref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.naquestionset":
        x[MIMETYPE] = "application/vnd.nextthought.questionsetref"


def internalization_questionref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.naquestion":
        x[MIMETYPE] = "application/vnd.nextthought.questionref"


def internalization_ntivideoref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.ntivideo":
        x[MIMETYPE] = "application/vnd.nextthought.ntivideoref"


def internalization_ntiaudioref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.ntiaudio":
        x[MIMETYPE] = "application/vnd.nextthought.ntiaudioref"


def internalization_discussionref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.discussion":
        x[MIMETYPE] = "application/vnd.nextthought.discussionref"


def internalization_ntislidedeckref_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType in SLIDE_DECK_MIME_TYPES:
        x[MIMETYPE] = SLIDE_DECK_REF_MIME_TYPES[0]


def is_time_line(x):
    result = False
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if not mimeType:
        if isinstance(x, Mapping):
            ntiid = x.get('ntiid') or x.get(NTIID)
        else:
            ntiid = None
        if ntiid and (JSON_TIMELINE in ntiid or is_ntiid_of_type(ntiid, TIMELINE)):
            result = True
    elif mimeType in TIMELINE_MIME_TYPES:
        result = True
    return result


def internalization_ntitimeline_pre_hook(k, x):
    if is_time_line(x):
        x[MIMETYPE] = TIMELINE_MIME_TYPES[0]


def internalization_ntitimelineref_pre_hook(k, x):
    if is_time_line(x):
        x[MIMETYPE] = TIMELINE_REF_MIME_TYPES[0]


def is_relatedwork_ref(x):
    result = False
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if not mimeType:
        if isinstance(x, Mapping):
            ntiid = x.get('ntiid') or x.get(NTIID)
        else:
            ntiid = None
        # check ntiid
        if      ntiid \
            and (   '.relatedworkref.' in ntiid
                 or is_ntiid_of_types(ntiid, (RELATED_WORK, RELATED_WORK_REF))):
            result = True
    elif mimeType in RELATED_WORK_REF_MIME_TYPES:
        result = True
    return result


def internalization_relatedworkref_pre_hook(k, x):
    if is_relatedwork_ref(x):
        x[MIMETYPE] = RELATED_WORK_REF_MIME_TYPES[0]


def internalization_relatedworkrefpointer_pre_hook(k, x):
    if is_relatedwork_ref(x):
        x[MIMETYPE] = RELATED_WORK_REF_POINTER_MIME_TYPES[0]


def internalization_mediaroll_pre_hook(k, x):
    if k == ITEMS and isinstance(x, MutableSequence):
        for item in x:
            internalization_ntiaudioref_pre_hook(None, item)
            internalization_ntivideoref_pre_hook(None, item)
internalization_ntiaudioroll_pre_hook = internalization_mediaroll_pre_hook


def internalization_videoroll_pre_hook(k, x):
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if mimeType == "application/vnd.nextthought.ntivideoroll":
        x[MIMETYPE] = "application/vnd.nextthought.videoroll"
    internalization_mediaroll_pre_hook(k, x)
internalization_audioroll_pre_hook = internalization_mediaroll_pre_hook


def internalization_nticourseoverviewgroup_pre_hook(k, x):
    if k == ITEMS and isinstance(x, MutableSequence):
        idx = 0
        while idx < len(x):
            item = x[idx]
            # Swizzle out our concrete mime types for refs.
            # don't include timelineref or relatedworkrefs pointers
            # as we need the definitions during import
            internalization_pollref_pre_hook(None, item)
            internalization_surveyref_pre_hook(None, item)
            internalization_ntiaudioref_pre_hook(None, item)
            internalization_ntivideoref_pre_hook(None, item)
            internalization_questionref_pre_hook(None, item)
            internalization_assignmentref_pre_hook(None, item)
            internalization_questionsetref_pre_hook(None, item)
            internalization_ntislidedeckref_pre_hook(None, item)

            # do checks
            mimeType = item.get(MIMETYPE) if isinstance(
                item, Mapping) else None

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
                # not yet ready
                elif not ntiids and not is_nti_course_bundle(iden):
                    del x[idx]
                    continue
                else:
                    internalization_discussionref_pre_hook(None, item)

            # handle media rolls
            if mimeType in ALL_MEDIA_ROLL_MIME_TYPES:
                internalization_mediaroll_pre_hook(ITEMS, item.get(ITEMS))

            # check next
            idx += 1


def internalization_ntilessonoverview_pre_hook(k, x):
    if k == ITEMS and isinstance(x, MutableSequence):
        for item in x:
            items = item.get(ITEMS) if isinstance(item, Mapping) else None
            if items is not None:
                internalization_nticourseoverviewgroup_pre_hook(ITEMS, items)


# lesson constraints


@interface.implementer(IInternalObjectUpdater)
@component.adapter(ILessonPublicationConstraints)
class _LessonPublicationConstraintsUpdater(InterfaceObjectIO):

    _ext_iface_upper_bound = ILessonPublicationConstraints

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        result = super(_LessonPublicationConstraintsUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        items = parsed.get(ITEMS)
        for ext_obj in items or ():
            if isinstance(ext_obj, Mapping):
                item = find_factory_for(ext_obj)()
                update_from_external_object(item, ext_obj, *args, **kwargs)
            else:
                item = ext_obj
            if ILessonPublicationConstraint.providedBy(item):
                self._ext_self.append(item)
        return result
