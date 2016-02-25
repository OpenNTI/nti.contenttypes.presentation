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

from nti.contenttypes.presentation import FIELDS
from nti.contenttypes.presentation import ACCEPTS
from nti.contenttypes.presentation import SLIDE_MIMETYES
from nti.contenttypes.presentation import SLIDE_VIDEO_MIMETYES

from nti.contenttypes.presentation._base import make_schema

from nti.contenttypes.presentation.interfaces import INTISlide
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

from nti.schema.interfaces import IVariant
from nti.schema.jsonschema import JsonSchemafier
from nti.schema.jsonschema import ui_type_from_field
from nti.schema.jsonschema import ui_type_from_field_iface
from nti.schema.jsonschema import interface_to_ui_type as iface_2_ui_type

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
            base = ui_type_from_field_iface(field.schema) or iface_2_ui_type(field.schema)
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
        accepts[SLIDE_MIMETYES[0]] = make_schema(schema=INTISlide).get(FIELDS)
        accepts[SLIDE_VIDEO_MIMETYES[0]] = make_schema(schema=INTISlideVideo).get(FIELDS)
        return result
