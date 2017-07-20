#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from persistent.list import PersistentList

from nti.contenttypes.presentation.interfaces import IAssetRef
from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIMedia
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIMediaRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import IConcreteAsset
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTITimelineRef
from nti.contenttypes.presentation.interfaces import INTISlideDeckRef
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef
from nti.contenttypes.presentation.interfaces import ITranscriptContainer
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRefPointer

from nti.contenttypes.presentation.media import NTIAudioRef
from nti.contenttypes.presentation.media import NTIVideoRef

from nti.contenttypes.presentation.relatedwork import NTIRelatedWorkRefPointer

from nti.contenttypes.presentation.slide import NTISlideDeckRef

from nti.contenttypes.presentation.timeline import NTITimeLineRef


@component.adapter(INTIVideo)
@interface.implementer(INTIVideoRef)
def ntivideo_to_ntivideoref(video):
    result = NTIVideoRef(target=video.ntiid,
                         poster=video.title,
                         label=video.title)
    result.byline = video.byline
    result.creator = video.creator
    return result


@component.adapter(INTIAudio)
@interface.implementer(INTIAudioRef)
def ntiaudio_to_ntiaudioref(audio):
    result = NTIAudioRef(target=audio.ntiid)
    result.byline = audio.byline
    result.creator = audio.creator
    return result


@component.adapter(INTIMedia)
@interface.implementer(INTIMediaRef)
def ntimedia_to_ntimediaref(media):
    if INTIAudio.providedBy(media):
        result = INTIAudioRef(media)
    else:
        result = INTIVideoRef(media)
    return result


@component.adapter(INTISlideDeck)
@interface.implementer(INTISlideDeckRef)
def slideck_to_ntislideckref(slideck):
    result = NTISlideDeckRef(target=slideck.ntiid)
    result.byline = slideck.byline
    result.creator = slideck.creator
    return result


@component.adapter(INTITimeline)
@interface.implementer(INTITimelineRef)
def timeline_to_ntitimelineref(timeline):
    result = NTITimeLineRef(target=timeline.ntiid)
    result.byline = timeline.byline
    result.creator = timeline.creator
    return result


@component.adapter(INTIRelatedWorkRef)
@interface.implementer(INTIRelatedWorkRefPointer)
def relatedworkref_to_relatedworkrefpointer(context):
    result = NTIRelatedWorkRefPointer(target=context.ntiid)
    result.byline = context.byline
    result.creator = context.creator
    return result


@interface.implementer(IAssetRef)
@component.adapter(IConcreteAsset)
def concrete_to_reference(context):
    if INTIRelatedWorkRef.providedBy(context):
        result = INTIRelatedWorkRefPointer(context)
    elif INTITimeline.providedBy(context):
        result = INTITimelineRef(context)
    elif INTISlideDeck.providedBy(context):
        result = INTISlideDeckRef(context)
    elif INTIAudio.providedBy(context):
        result = INTIAudioRef(context)
    elif INTIVideo.providedBy(context):
        result = INTIVideoRef(context)
    else:
        result = None
    return result


@component.adapter(INTIMedia)
@interface.implementer(ITranscriptContainer)
class TranscriptContainer(object):

    def __init__(self, context):
        self.context = context

    def clear(self):
        for obj in self.context.transcripts or ():
            obj.__parent__ = None
        if self.context.transcripts:
            del self.context.transcripts[:]

    def add(self, transcript):
        assert INTITranscript.providedBy(transcript)
        if not self.context.transcripts:
            self.context.transcripts = PersistentList()
        transcript.__parent__ = self.context
        self.context.transcripts.append(transcript)

    def remove(self, transcript):
        assert INTITranscript.providedBy(transcript)
        try:
            if self.context.transcripts is not None:
                self.context.transcripts.remove(transcript)
                transcript.__parent__ = None
                return True
        except ValueError:
            pass
        return False

    def __getitem__(self, index):
        return self.context.transcripts[index]

    def __len__(self):
        return len(self.context.transcripts or ())

    def __iter__(self):
        return iter(self.context.transcripts or ())
