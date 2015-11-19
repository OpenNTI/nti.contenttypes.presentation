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

from nti.common.property import alias

from nti.ntiids.ntiids import TYPE_UUID
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from nti.wref.interfaces import IWeakRef

from ._base import PersistentPresentationAsset

from .interfaces import INTICourseOverviewGroup

from . import NTI_COURSE_OVERVIEW_GROUP

@EqHash('ntiid')
@interface.implementer(INTICourseOverviewGroup)
class NTICourseOverViewGroup(PersistentPresentationAsset):
	createDirectFieldProperties(INTICourseOverviewGroup)

	__external_class_name__ = u"CourseOverviewGroup"
	mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewgroup"
	
	items = alias('Items')
	color = alias('accentColor')

	@readproperty
	def ntiid(self):
		digest = md5(str(uuid.uuid4())).hexdigest()
		specific = make_specific_safe(TYPE_UUID + ".%s" % digest)
		result = make_ntiid(provider='NTI',
							nttype=NTI_COURSE_OVERVIEW_GROUP,
							specific=specific)
		self.ntiid = result
		return result
	
	def __getitem__(self, index):
		item = self.items[index]
		return item
	
	def __setitem__(self, index, item):
		self.items[index] = item
	
	def __len__(self):
		result = len(self.items or ()) # include weak refs
		return result

	def __iter__(self):
		for item in self.items or ():
			resolved = item() if IWeakRef.providedBy(item) else item
			if resolved is not None:
				yield resolved
			else:
				logger.warn("Cannot resolve %s", item)
	
	def pop(self, index):
		self.items.pop(index)

	def remove(self, item):
		try:
			if self.items:
				self.items.remove(item)
				return True
		except ValueError:
			pass
		return False
