#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.common.property import alias

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTIRelatedWorkRef

@EqHash('ntiid')
@interface.implementer(INTIRelatedWorkRef)
class NTIRelatedWorkRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIRelatedWorkRef)

	__external_class_name__ = u"RelatedWork"
	mime_type = mimeType = u'application/vnd.nextthought.relatedworkref'

	Creator = alias('creator')
	desc = alias('description')
	target_ntiid = alias('target')
	targetMimeType = target_mime_type = alias('type')

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
	"Import from NTIRelatedWorkRef instead",
	NTIRelatedWork='nnti.contenttypes.presentation.relatedwork:NTIRelatedWorkRef')
