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

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.container.contained import Contained

from zope.mimetype.interfaces import IContentTypeAware

from nti.coremetadata.interfaces import ICreated

from nti.coremetadata.mixins import RecordableMixin

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.externalization.representation import WithRepr

from nti.ntiids.ntiids import TYPE_UUID
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

from nti.schema.field import SchemaConfigured

from .interfaces import IPresentationAsset

class PersistentMixin(SchemaConfigured,
					  PersistentCreatedModDateTrackingObject):

	parameters = {} # IContentTypeAware

	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentCreatedModDateTrackingObject.__init__(self, *args, **kwargs)

@WithRepr
@interface.implementer(IPresentationAsset, IContentTypeAware, ICreated)
class PersistentPresentationAsset(PersistentMixin,
								  RecordableMixin,
								  Contained):  # order matters
	title = None
	byline = None
	description = None

	@readproperty
	def creator(self):
		return self.byline

	@classmethod
	def generate_ntiid(cls, nttype):
		digest = md5(str(uuid.uuid4())).hexdigest()
		specific = make_specific_safe(TYPE_UUID + ".%s" % digest)
		result = make_ntiid(provider='NTI',
							nttype=nttype,
							specific=specific)
		return result
