#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import Lazy
from zope.cachedescriptors.property import readproperty

from zope.mimetype.interfaces import IContentTypeAware

from persistent.list import PersistentList

from nti.base.interfaces import IFile

from nti.contenttypes.presentation import NTI_AUDIO
from nti.contenttypes.presentation import NTI_VIDEO
from nti.contenttypes.presentation import NTI_AUDIO_REF
from nti.contenttypes.presentation import NTI_VIDEO_REF
from nti.contenttypes.presentation import NTI_AUDIO_ROLL
from nti.contenttypes.presentation import NTI_VIDEO_ROLL
from nti.contenttypes.presentation import NTI_TRANSCRIPT
from nti.contenttypes.presentation import NTI_AUDIO_SOURCE
from nti.contenttypes.presentation import NTI_VIDEO_SOURCE
from nti.contenttypes.presentation import NTI_TRANSCRIPT_MIMETYPE

from nti.contenttypes.presentation.common import make_schema

from nti.contenttypes.presentation.interfaces import EVERYONE
from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIMedia
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIMediaRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIAudioSource
from nti.contenttypes.presentation.interfaces import INTIVideoSource

from nti.contenttypes.presentation.mixin import PersistentMixin
from nti.contenttypes.presentation.mixin import RecordablePresentationAsset

from nti.property.property import alias

from nti.ntiids.ntiids import get_parts
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

from nti.schema.fieldproperty import createDirectFieldProperties


def compute_part_ntiid(part, nttype, field):
    parent = part.__parent__
    base_ntiid = getattr(parent, 'ntiid', None)
    parent_parts = getattr(parent, field, None) or None
    if base_ntiid and parent_parts:
        # Gather all child parts ntiids.
        parent_part_ids = set()
        for child_part in parent_parts or ():
            child_part_ntiid = child_part.__dict__.get('ntiid')
            parent_part_ids.add(child_part_ntiid)
        parent_part_ids.discard(None)

        uid = make_specific_safe(str(0))
        parts = get_parts(base_ntiid)

        # Iterate until we find an ntiid that does not collide.
        idx = 0
        while True:
            specific = "%s.%s" % (parts.specific, uid)
            result = make_ntiid(parts.date,
                                parts.provider,
                                nttype,
                                specific)
            if result not in parent_part_ids:
                break
            idx += 1
            uid = idx
        return result
    return None


@interface.implementer(INTITranscript, IContentTypeAware)
class NTITranscript(PersistentMixin):
    createDirectFieldProperties(INTITranscript)

    __external_class_name__ = "Transcript"
    mime_type = mimeType = NTI_TRANSCRIPT_MIMETYPE

    @Lazy
    def ntiid(self):
        return compute_part_ntiid(self, NTI_TRANSCRIPT, 'transcripts')

    def schema(self):
        return make_schema(schema=INTITranscript)

    def is_source_attached(self):
        return IFile.providedBy(self.src)

    def __setattr__(self, name, value):
        PersistentMixin.__setattr__(self, name, value)
        if name == 'src' and IFile.providedBy(value):
            value.__parent__ = self  # take ownership


@interface.implementer(INTIAudioSource, IContentTypeAware)
class NTIAudioSource(PersistentMixin):
    createDirectFieldProperties(INTIAudioSource)

    __external_class_name__ = "VideoSource"
    mime_type = mimeType = 'application/vnd.nextthought.ntiaudiosource'

    @Lazy
    def ntiid(self):
        return compute_part_ntiid(self, NTI_AUDIO_SOURCE, 'sources')

    def schema(self):
        result = make_schema(schema=INTIAudioSource)
        return result


@interface.implementer(INTIVideoSource, IContentTypeAware)
class NTIVideoSource(PersistentMixin):
    createDirectFieldProperties(INTIVideoSource)

    __external_class_name__ = "VideoSource"
    mime_type = mimeType = 'application/vnd.nextthought.ntivideosource'

    @Lazy
    def ntiid(self):
        return compute_part_ntiid(self, NTI_VIDEO_SOURCE, 'sources')

    def schema(self):
        result = make_schema(schema=INTIVideoSource)
        return result


@total_ordering
@interface.implementer(INTIMedia)
class NTIMedia(RecordablePresentationAsset):
    createDirectFieldProperties(INTIMedia)

    __external_class_name__ = "Media"
    mime_type = mimeType = 'application/vnd.nextthought.ntimedia'

    nttype = u'NTIMedia'
    Creator = alias('creator')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(self.nttype)
        return self.ntiid

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented


@interface.implementer(INTIMediaRef)
class NTIMediaRef(RecordablePresentationAsset):
    createDirectFieldProperties(INTIMediaRef)

    __external_class_name__ = "MediaRef"
    mime_type = mimeType = 'application/vnd.nextthought.ntimediaref'

    nttype = u'NTIMediaRef'
    visibility = EVERYONE
    Creator = alias('creator')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(self.nttype)
        return self.ntiid

    @readproperty
    def target(self):
        return self.ntiid


@interface.implementer(INTIVideo)
class NTIVideo(NTIMedia):
    createDirectFieldProperties(INTIVideo)

    __external_class_name__ = "Video"
    mime_type = mimeType = 'application/vnd.nextthought.ntivideo'

    closedCaption = closedCaptions = alias('closed_caption')

    nttype = NTI_VIDEO

    def __setattr__(self, name, value):
        super(NTIVideo, self).__setattr__(name, value)
        if name in ("sources", "transcripts"):
            for x in getattr(self, name, None) or ():
                x.__parent__ = self  # take ownership


@interface.implementer(INTIVideoRef)
class NTIVideoRef(NTIMediaRef):  # not recordable
    createDirectFieldProperties(INTIVideoRef)

    __external_class_name__ = "Video"
    mime_type = mimeType = 'application/vnd.nextthought.ntivideoref'

    nttype = NTI_VIDEO_REF


@interface.implementer(INTIAudio)
class NTIAudio(NTIMedia):
    createDirectFieldProperties(INTIAudio)

    __external_class_name__ = "Audio"
    mime_type = mimeType = 'application/vnd.nextthought.ntiaudio'

    nttype = NTI_AUDIO

    def __setattr__(self, name, value):
        super(NTIAudio, self).__setattr__(name, value)
        if name in ("sources", "transcripts"):
            for x in getattr(self, name, None) or ():
                x.__parent__ = self  # take ownership


@interface.implementer(INTIAudioRef)
class NTIAudioRef(NTIMediaRef):  # not recordable
    createDirectFieldProperties(INTIAudioRef)

    __external_class_name__ = "Audio"
    mime_type = mimeType = 'application/vnd.nextthought.ntiaudioref'

    nttype = NTI_AUDIO_REF


@interface.implementer(INTIMediaRoll)
class NTIMediaRoll(RecordablePresentationAsset):
    createDirectFieldProperties(INTIMediaRoll)

    __external_class_name__ = "MediaRoll"
    mime_type = mimeType = 'application/vnd.nextthought.ntimediaroll'

    jsonschema = 'mediaroll'

    items = alias('Items')
    Creator = alias('creator')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(self.nttype)
        return self.ntiid

    def __getitem__(self, index):
        item = self.items[index]
        return item

    def __setitem__(self, index, item):
        assert INTIMediaRef.providedBy(item)
        item.__parent__ = self  # take ownership
        self.items[index] = item

    def __len__(self):
        result = len(self.items or ())  # include weak refs
        return result

    def __iter__(self):
        return iter(self.items or ())

    def __contains__(self, obj):
        ntiid = getattr(obj, 'ntiid', None) or str(obj)
        for item in self:
            if item.ntiid == ntiid:
                return True
        return False

    def append(self, item):
        assert INTIMediaRef.providedBy(item)
        item.__parent__ = self  # take ownership
        self.items = PersistentList() if self.items is None else self.items
        self.items.append(item)
    add = append

    def pop(self, index):
        self.items.pop(index)

    def insert(self, index, obj):
        # Remove from our list if it exists, and then insert at.
        self.remove(obj)
        if index is None or index >= len(self):
            # Default to append.
            self.append(obj)
        else:
            obj.__parent__ = self  # take ownership
            self.items.insert(index, obj)

    def remove(self, item):
        try:
            self.items.remove(item)
            return True
        except (AttributeError, ValueError):
            pass
        return False

    def reset(self, *args, **kwargs):
        result = len(self)
        if self.items:
            del self.items[:]
        return result
    clear = reset


@interface.implementer(INTIAudioRoll)
class NTIAudioRoll(NTIMediaRoll):
    createDirectFieldProperties(INTIAudioRoll)

    nttype = NTI_AUDIO_ROLL
    __external_class_name__ = "AudioRoll"
    mime_type = mimeType = 'application/vnd.nextthought.ntiaudioroll'

    jsonschema = 'audioroll'


@interface.implementer(INTIVideoRoll)
class NTIVideoRoll(NTIMediaRoll):
    createDirectFieldProperties(INTIVideoRoll)

    nttype = NTI_VIDEO_ROLL
    # For legacy reasons, these are the classes need for IPAD
    # and mimetype needed for the webapp to match up.
    __external_class_name__ = "ContentVideoCollection"
    mime_type = mimeType = 'application/vnd.nextthought.videoroll'

    jsonschema = 'videoroll'


def media_to_mediaref(media):
    if INTIAudio.providedBy(media):
        result = INTIAudioRef(media)
    else:
        result = INTIVideoRef(media)
    return result
