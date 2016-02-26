#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import uuid
from hashlib import md5

from zope import component

from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemafier

from nti.ntiids.ntiids import TYPE_UUID
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

def generate_ntiid(nttype):
	digest = md5(str(uuid.uuid4())).hexdigest()
	specific = make_specific_safe(TYPE_UUID + ".%s" % digest)
	result = make_ntiid(provider='NTI',
						nttype=nttype,
						specific=specific)
	return result

def make_schema(schema):
	name = schema.queryTaggedValue('_ext_jsonschema') or u''
	schemafier = component.getUtility(IPresentationAssetJsonSchemafier, name=name)
	result = schemafier.make_schema(schema=schema)
	return result
