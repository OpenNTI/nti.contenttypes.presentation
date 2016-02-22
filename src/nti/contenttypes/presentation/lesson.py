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

from persistent.list import PersistentList

from nti.common.property import alias

from nti.contenttypes.presentation import NTI_COURSE_OVERVIEW_SPACER

from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTICourseOverviewSpacer

from nti.coremetadata.mixins import CalendarPublishableMixin
from nti.coremetadata.mixins import RecordableContainerMixin

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import EqHash

@EqHash('ntiid')
@interface.implementer(INTICourseOverviewSpacer)
class NTICourseOverViewSpacer(PersistentPresentationAsset):
	createDirectFieldProperties(INTICourseOverviewSpacer)

	__external_class_name__ = u"CourseOverviewSpacer"
	mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewspacer"

	@readproperty
	def ntiid(self):
		result = self.generate_ntiid(NTI_COURSE_OVERVIEW_SPACER)
		self.ntiid = result
		return result

@total_ordering
@EqHash('ntiid')
@interface.implementer(INTILessonOverview)
class NTILessonOverView(CalendarPublishableMixin,
						RecordableContainerMixin,
						PersistentPresentationAsset):
	createDirectFieldProperties(INTILessonOverview)

	__external_class_name__ = u"LessonOverView"
	mime_type = mimeType = u"application/vnd.nextthought.ntilessonoverview"

	items = alias('Items')

	__name__ = alias('ntiid')

	def __getitem__(self, index):
		return self.items[index]

	def __setitem__(self, index, item):
		assert INTICourseOverviewGroup.providedBy(item)
		item.__parent__ = self  # take ownership
		self.items[index] = item

	def __len__(self):
		return len(self.items or ())

	def __iter__(self):
		return iter(self.items or ())

	def __contains__(self, obj):
		ntiid = getattr(obj, 'ntiid', None) or str(obj)
		for item in self:
			if item.ntiid == ntiid:
				return True
		return False

	def append(self, group):
		assert INTICourseOverviewGroup.providedBy(group)
		group.__parent__ = self  # take ownership
		self.items = PersistentList() if self.items is None else self.items
		self.items.append(group)
	add = append

	def insert(self, index, obj):
		# Remove from our list if it exists, and then insert at.
		self.remove(obj)
		if index is None or index >= len(self):
			# Default to append.
			self.append(obj)
		else:
			obj.__parent__ = self  # take ownership
			self.items.insert(index, obj)

	def pop(self, index):
		self.items.pop(index)

	def remove(self, group):
		try:
			self.items.remove(group)
			return True
		except (AttributeError, ValueError):
			pass
		return False

	def reset(self, *args, **kwargs):
		result = len(self)
		if self.items:
			del self.items[:]
		return result
	clear = reset
	
	def __lt__(self, other):
		try:
			return (self.mimeType, self.title) < (other.mimeType, other.title)
		except AttributeError:
			return NotImplemented

	def __gt__(self, other):
		try:
			return (self.mimeType, self.title) > (other.mimeType, other.title)
		except AttributeError:
			return NotImplemented

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
	"moved to nti.contenttypes.presentation.group",
	"nti.contenttypes.presentation.group",
	"NTICourseOverViewGroup")
