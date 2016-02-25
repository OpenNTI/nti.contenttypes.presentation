#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.schema.interfaces import IList
from zope.schema.interfaces import IObject

from nti.contenttypes.presentation import FIELDS, GROUP_OVERVIEWABLE_INTERFACES
from nti.contenttypes.presentation import ACCEPTS
from nti.contenttypes.presentation import MEDIA_REF_INTERFACES
from nti.contenttypes.presentation import interface_to_mime_type

from nti.contenttypes.presentation._base import make_schema

from nti.contenttypes.presentation.interfaces import INTISlide,\
    INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemafier

from nti.coremetadata.interfaces import ICreated
from nti.coremetadata.interfaces import IRecordable
from nti.coremetadata.interfaces import ICreatedTime
from nti.coremetadata.interfaces import ILastModified
from nti.coremetadata.interfaces import IRecordableContainer

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.schema.interfaces import IVariant
from nti.schema.jsonschema import JsonSchemafier
from nti.schema.jsonschema import ui_type_from_field
from nti.schema.jsonschema import ui_type_from_field_iface
from nti.schema.jsonschema import interface_to_ui_type as iface_2_ui_type

ITEMS = StandardExternalFields.ITEMS

class BaseJsonSchemafier(JsonSchemafier):

    def allow_field(self, name, field):
        if     name.startswith('_') \
            or name in ICreated \
            or name in IRecordable \
            or name in ICreatedTime \
            or name in ILastModified \
            or name in IRecordableContainer \
            or field.queryTaggedValue('_ext_excluded_out'):
            return False
        return True

    def _process_object(self, field):
        if      IObject.providedBy(field) \
            and field.schema is not interface.Interface:
            base =      interface_to_mime_type().get(field.schema) \
                    or  ui_type_from_field_iface(field.schema) \
                    or  iface_2_ui_type(field.schema)
            return base
        return None

    def _process_variant(self, field, ui_type):
        base_types = set()
        for field in field.fields:
            base = ui_type_from_field(field)[1]
            if not base:
                base = self._process_object(field)
            if base:
                base_types.add(base.lower())
        if base_types:
            base_types = sorted(base_types, reverse=True)
            ui_base_type = base_types[0] if len(base_types) == 1 else base_types
        else:
            ui_base_type = ui_type
        return ui_base_type

    def ui_types_from_field(self, field):
        ui_type, ui_base_type = super(BaseJsonSchemafier, self).ui_types_from_field(field)
        if IVariant.providedBy(field) and not ui_base_type:
            ui_base_type = self._process_variant(field, ui_type)
        elif IList.providedBy(field) and not ui_base_type:
            if IObject.providedBy(field.value_type):
                ui_base_type = self._process_object(field.value_type)
            elif IVariant.providedBy(field.value_type):
                ui_base_type = self._process_variant(field, ui_type)
        return ui_type, ui_base_type

@interface.implementer(IPresentationAssetJsonSchemafier)
class PresentationAssetJsonSchemafier(object):
    
    def make_schema(self, schema=IPresentationAsset):
        result = LocatedExternalDict()
        maker = BaseJsonSchemafier(schema)
        result[FIELDS] = maker.make_schema()
        return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class SlideDeckJsonSchemafier(PresentationAssetJsonSchemafier):
    
    def make_schema(self, schema=INTISlideDeck):
        result = super(SlideDeckJsonSchemafier, self).make_schema(INTISlideDeck)
        accepts = result[ACCEPTS] = {}
        for iface in (INTISlide, INTISlideVideo):
            accepts[interface_to_mime_type().get(iface)] = make_schema(schema=iface).get(FIELDS)
        return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class MediaRollJsonSchemafier(PresentationAssetJsonSchemafier):
    
    ref_interfaces = MEDIA_REF_INTERFACES
        
    def make_schema(self, schema=INTIMediaRoll):
        result = super(MediaRollJsonSchemafier, self).make_schema(schema)
        accepts = result[ACCEPTS] = {}
        for iface in self.ref_interfaces:
            accepts[interface_to_mime_type().get(iface)] = make_schema(schema=iface).get(FIELDS)
        fields = result[FIELDS]
        base_types = sorted(accepts.keys())
        fields[ITEMS]['base_type'] = base_types if len(base_types) > 1 else base_types[0]
        return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class VideoRollJsonSchemafier(MediaRollJsonSchemafier):
    
    ref_interfaces = (INTIVideoRef,)
    
    def make_schema(self, schema=INTIVideoRoll):
        result = super(VideoRollJsonSchemafier, self).make_schema(INTIVideoRoll)
        return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class AudioRollJsonSchemafier(MediaRollJsonSchemafier):
    
    ref_interfaces = (INTIAudioRef,)
    
    def make_schema(self, schema=INTIAudioRoll):
        result = super(AudioRollJsonSchemafier, self).make_schema(INTIAudioRoll)
        return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class CourseOverviewGroupJsonSchemafier(PresentationAssetJsonSchemafier):
    
    ref_interfaces = GROUP_OVERVIEWABLE_INTERFACES
    
    def make_schema(self, schema=INTICourseOverviewGroup):
        result = super(CourseOverviewGroupJsonSchemafier, self).make_schema(INTICourseOverviewGroup)
        accepts = result[ACCEPTS] = {}
        for iface in self.ref_interfaces:
            accepts[interface_to_mime_type().get(iface)] = make_schema(schema=iface).get(FIELDS)
        fields = result[FIELDS]
        fields[ITEMS]['base_type'] = sorted(accepts.keys())
        return result
