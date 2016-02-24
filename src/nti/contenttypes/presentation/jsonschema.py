#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division

__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.schema.interfaces import IObject

from nti.contenttypes.presentation import FIELDS

from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemafier

from nti.coremetadata.interfaces import ICreatedTime
from nti.coremetadata.interfaces import ILastModified

from nti.externalization.interfaces import LocatedExternalDict

from nti.schema.interfaces import IVariant
from nti.schema.jsonschema import JsonSchemafier
from nti.schema.jsonschema import ui_type_from_field
from nti.schema.jsonschema import ui_type_from_field_iface
from nti.schema.jsonschema import iface_ui_type as interface_ui_type

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
            base_types = set()
            for field in field.fields:
                base = ui_type_from_field(field)[1]
                if not base and IObject.providedBy(field):
                    base =   ui_type_from_field_iface(field.schema) \
                          or interface_ui_type(field.schema)  
                if base and base not in ("nterface",):
                    base_types.add(base.lower())
            if base_types:
                base_types = sorted(base_types, reverse=True)
                ui_base_type = base_types[0] if len(base_types) == 1 else base_types
            else:
                ui_base_type = ui_type
        return ui_type, ui_base_type

@interface.implementer(IPresentationAssetJsonSchemafier)
class PresentationAssetJsonSchemafier(object):
    
    def make_schema(self, schema=IPresentationAsset):
        result = LocatedExternalDict()
        maker = BaseJsonSchemafier(schema)
        result[FIELDS] = maker.make_schema()
        return result
