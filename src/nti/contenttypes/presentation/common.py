#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import re
import uuid

from zope import component
from zope import interface

from nti.contenttypes.presentation.interfaces import CREDIT
from nti.contenttypes.presentation.interfaces import EVERYONE

from nti.contenttypes.presentation.interfaces import IVisibilityOptionsProvider
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemaMaker

from nti.coremetadata.utils import make_schema as core_schema_maker

from nti.ntiids.ntiids import TYPE_UUID
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

def generate_ntiid(nttype, provider='NTI'):
	digest = re.sub('-', '', str(uuid.uuid4())).upper()
	specific = make_specific_safe(TYPE_UUID + ".%s" % digest)
	result = make_ntiid(provider=provider,
						nttype=nttype,
						specific=specific)
	return result

def make_schema(schema, user=None):
	result = core_schema_maker(schema, user=user, maker=IPresentationAssetJsonSchemaMaker)
	return result

@interface.implementer(IVisibilityOptionsProvider)
class DefaultVisibilityOptionProvider(object):

	def __init__(self, *args):
		pass

	def iter_options(self):
		result = (EVERYONE, CREDIT) 
		return result

def get_visibility_options():
	result = set()
	for _, provider in list(component.getUtilitiesFor(IVisibilityOptionsProvider)):
		result.update(provider.iter_options())
	return tuple(result)
