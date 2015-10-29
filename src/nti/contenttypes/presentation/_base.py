#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.container.contained import Contained

from zope.mimetype.interfaces import IContentTypeAware

from nti.coremetadata.mixins import RecordableMixin

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.externalization.representation import WithRepr

from nti.schema.field import SchemaConfigured

from .interfaces import IPresentationAsset

class PersistentMixin(SchemaConfigured,
					  PersistentCreatedModDateTrackingObject,
					  Contained):

	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentCreatedModDateTrackingObject.__init__(self, *args, **kwargs)

@WithRepr
@interface.implementer(IPresentationAsset, IContentTypeAware)
class PersistentPresentationAsset(PersistentMixin, RecordableMixin): # order matters
	parameters = {}
	creator = None
