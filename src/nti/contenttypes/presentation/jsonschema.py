#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ISequence

from nti.contenttypes.presentation import FIELDS
from nti.contenttypes.presentation import ACCEPTS
from nti.contenttypes.presentation import MEDIA_REF_INTERFACES
from nti.contenttypes.presentation import GROUP_OVERVIEWABLE_INTERFACES

from nti.contenttypes.presentation.common import make_schema
from nti.contenttypes.presentation.common import get_visibility_options

from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTISlide
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIAudioSource
from nti.contenttypes.presentation.interfaces import INTIVideoSource
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemaMaker

from nti.contenttypes.presentation.schema import VisibilityField

from nti.coremetadata.jsonschema import CoreJsonSchemafier

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.recorder.interfaces import IRecordable
from nti.recorder.interfaces import IRecordableContainer

from nti.schema.interfaces import IVariant

ITEMS = StandardExternalFields.ITEMS

logger = __import__('logging').getLogger(__name__)


class BaseJsonSchemafier(CoreJsonSchemafier):

    IGNORE_INTERFACES = CoreJsonSchemafier.IGNORE_INTERFACES + \
                        (IRecordable, IRecordableContainer)

    def post_process_field(self, name, field, item_schema):
        CoreJsonSchemafier.post_process_field(self, name, field, item_schema)
        if isinstance(field, VisibilityField):
            item_schema['type'] = 'Choice'
            item_schema['choices'] = sorted(get_visibility_options())


class MediaSourceJsonSchemafier(BaseJsonSchemafier):

    def post_process_field(self, name, field, item_schema):
        BaseJsonSchemafier.post_process_field(self, name, field, item_schema)
        # handle type field
        if      name == 'type' \
            and ISequence.providedBy(field) \
            and IChoice.providedBy(field.value_type):
            choices, _ = self.get_data_from_choice_field(field.value_type)
            item_schema['choices'] = sorted(choices)
        # handle source field
        if      name == 'source' \
            and ISequence.providedBy(field) \
            and IVariant.providedBy(field.value_type):
            for x in field.value_type.fields:
                if IChoice.providedBy(x):
                    choices, _ = self.get_data_from_choice_field(x)
                    item_schema['choices'] = sorted(choices)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class PresentationAssetJsonSchemaMaker(object):

    maker = BaseJsonSchemafier

    def make_schema(self, schema=IPresentationAsset, unused_user=None):
        result = LocatedExternalDict()
        maker = self.maker(schema)
        result[FIELDS] = maker.make_schema()
        return result


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class ItemContainerJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

    has_items = True
    ref_interfaces = ()

    def make_schema(self, schema=IPresentationAsset, user=None):
        result = PresentationAssetJsonSchemaMaker.make_schema(self, schema, user)
        accepts = result[ACCEPTS] = {}
        for iface in self.ref_interfaces:
            mimeType = iface.getTaggedValue('_ext_mime_type')
            accepts[mimeType] = make_schema(schema=iface).get(FIELDS)
        if self.has_items:
            fields = result[FIELDS]
            base_types = sorted(accepts.keys())
            base_type = base_types if len(base_types) > 1 else base_types[0]
            fields[ITEMS]['base_type'] = base_type
        return result


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class SlideDeckJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    has_items = False
    ref_interfaces = (INTISlide, INTISlideVideo)

    def make_schema(self, unused_schema=INTISlideDeck, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTISlideDeck, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

    maker = MediaSourceJsonSchemafier

    def make_schema(self, unused_schema=INTIAudioSource, user=None):
        return PresentationAssetJsonSchemaMaker.make_schema(self, INTIAudioSource, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

    maker = MediaSourceJsonSchemafier

    def make_schema(self, unused_schema=INTIVideoSource, user=None):
        return PresentationAssetJsonSchemaMaker.make_schema(self, INTIVideoSource, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    has_items = False
    ref_interfaces = (INTITranscript, INTIVideoSource)

    def make_schema(self, unused_schema=INTIVideo, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTIVideo, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    has_items = False
    ref_interfaces = (INTITranscript, INTIAudioSource)

    def make_schema(self, unused_schema=INTIAudio, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTIAudio, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class MediaRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    ref_interfaces = MEDIA_REF_INTERFACES

    def make_schema(self, unused_schema=INTIMediaRoll, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTIMediaRoll, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    ref_interfaces = (INTIVideoRef,)

    def make_schema(self, unused_schema=INTIVideoRoll, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTIVideoRoll, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    ref_interfaces = (INTIAudioRef,)

    def make_schema(self, unused_schema=INTIAudioRoll, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTIAudioRoll, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class CourseOverviewGroupJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    ref_interfaces = GROUP_OVERVIEWABLE_INTERFACES

    def make_schema(self, unused_schema=INTICourseOverviewGroup, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTICourseOverviewGroup, user)


@interface.implementer(IPresentationAssetJsonSchemaMaker)
class LessonOverviewJsonSchemaMaker(ItemContainerJsonSchemaMaker):

    ref_interfaces = (INTICourseOverviewGroup,)

    def make_schema(self, unused_schema=INTILessonOverview, user=None):
        return ItemContainerJsonSchemaMaker.make_schema(self, INTILessonOverview, user)
