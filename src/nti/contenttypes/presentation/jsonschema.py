#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.schema.jsonschema import JsonSchemafier

class BaseJsonSchemafier(JsonSchemafier):

    def allow_field(self, name, field):
        if name.startswith('_'):
            return False
        return True
