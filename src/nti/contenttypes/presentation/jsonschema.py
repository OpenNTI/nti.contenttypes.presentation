#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemafier

from nti.coremetadata.interfaces import ICreatedTime
from nti.coremetadata.interfaces import ILastModified

from nti.schema.interfaces import IVariant
from nti.schema.jsonschema import JsonSchemafier
from nti.schema.jsonschema import ui_type_from_field

class BaseJsonSchemafier(JsonSchemafier):

    def allow_field(self, name, field):
        if     name.startswith('_') \
            or name in ICreatedTime \
            or name in ILastModified:
            return False
        return True

    def ui_types_from_field(self, field):
        ui_type, ui_base_type = super(BaseJsonSchemafier, self).ui_types_from_field(field)
        if IVariant.providedBy(field) and not ui_base_type:
            base_types = map(lambda x:ui_type_from_field(x)[1], field.fields)
            if 'string' in base_types:
                ui_base_type = 'string'
        return ui_type, ui_base_type

@interface.implementer(IPresentationAssetJsonSchemafier)
class PresentationAssetJsonSchemafier(object):
    
    def make_schema(self, schema=IPresentationAsset):
        result = BaseJsonSchemafier(schema)
        return result.make_schema()
