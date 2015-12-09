#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.cachedescriptors.property import readproperty

from persistent.list import PersistentList

from nti.common.property import alias

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from nti.wref.interfaces import IWeakRef

from ._base import PersistentPresentationAsset

from .interfaces import IGroupOverViewable
from .interfaces import INTICourseOverviewGroup
from .interfaces import IGroupOverViewableWeakRef

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
		self.ntiid = self.generate_ntiid(NTI_COURSE_OVERVIEW_GROUP)
		return self.ntiid
	
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
	
	def append(self, item):
		assert IGroupOverViewable.providedBy(item) \
			or IGroupOverViewableWeakRef.providedBy(item)

		self.items = PersistentList() if self.items is None else self.items
		self.items.append(item)
	add = append
	
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
