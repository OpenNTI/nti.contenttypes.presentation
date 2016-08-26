#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.contenttypes.presentation import NTI_RELATED_WORK_REF
from nti.contenttypes.presentation import NTI_RELATED_WORK_REF_POINTER

from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRefPointer

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

@total_ordering
@EqHash('ntiid')
@interface.implementer(INTIRelatedWorkRef)
class NTIRelatedWorkRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIRelatedWorkRef)

	__external_class_name__ = u"RelatedWork"
	mime_type = mimeType = u'application/vnd.nextthought.relatedworkref'

	target = None
	
	Creator = alias('creator')
	desc = alias('description')
	target_ntiid = alias('target')
	targetMimeType = target_mime_type = alias('type')

	nttype = NTI_RELATED_WORK_REF

	__name__ = alias('ntiid')

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(self.nttype)
		return self.ntiid

	def __lt__(self, other):
		try:
			return (self.mimeType, self.label) < (other.mimeType, other.label)
		except AttributeError:
			return NotImplemented

	def __gt__(self, other):
		try:
			return (self.mimeType, self.label) > (other.mimeType, other.label)
		except AttributeError:
			return NotImplemented

@EqHash('ntiid')
@interface.implementer(INTIRelatedWorkRefPointer)
class NTIRelatedWorkRefPointer(PersistentPresentationAsset):
	createDirectFieldProperties(INTIRelatedWorkRefPointer)

	__external_class_name__ = u"RelatedWorkRefPointer"
	mime_type = mimeType = u'application/vnd.nextthought.relatedworkrefpointer'

	__name__ = alias('ntiid')

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(NTI_RELATED_WORK_REF_POINTER)
		return self.ntiid

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
	"Import from NTIRelatedWorkRef instead",
	NTIRelatedWork='nti.contenttypes.presentation.relatedwork:NTIRelatedWorkRef')
