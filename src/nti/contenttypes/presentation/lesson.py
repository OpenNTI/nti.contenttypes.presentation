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

from persistent.list import PersistentList

from nti.common.property import alias

from nti.coremetadata.mixins import CalendarPublishableMixin

from nti.ntiids.ntiids import make_ntiid

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewGroup
from .interfaces import INTICourseOverviewSpacer

from . import NTI_COURSE_OVERVIEW_SPACER

@EqHash('ntiid')
@interface.implementer(INTICourseOverviewSpacer)
class NTICourseOverViewSpacer(PersistentPresentationAsset):
	createDirectFieldProperties(INTICourseOverviewSpacer)

	__external_class_name__ = u"CourseOverviewSpacer"
	mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewspacer"

	@readproperty
	def ntiid(self):
		result = make_ntiid(provider='NTI',
							nttype=NTI_COURSE_OVERVIEW_SPACER,
							specific=md5(str(uuid.uuid4())).hexdigest())
		self.ntiid = result
		return result

@EqHash('ntiid')
@interface.implementer(INTILessonOverview)
class NTILessonOverView(PersistentPresentationAsset, CalendarPublishableMixin):
	createDirectFieldProperties(INTILessonOverview)

	__external_class_name__ = u"LessonOverView"
	mime_type = mimeType = u"application/vnd.nextthought.ntilessonoverview"

	items = alias('Items')

	def __getitem__(self, index):
		return self.items[index]

	def __setitem__(self, index, item):
		self.items[index] = item

	def __len__(self):
		return len(self.items or ())

	def __iter__(self):
		return iter(self.items or ())

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
			self.items.insert(index, obj)

	def pop(self, index):
		self.items.pop(index)

	def remove(self, group):
		try:
			if self.items:
				self.items.remove(group)
				return True
		except ValueError:
			pass
		return False

	def reset(self, event=True):
		result = len(self)
		if event:
			del self.items[:]
		else:
			del self.items.data[:]
	clear = reset

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
	"moved to nti.contenttypes.presentation.group",
	"nti.contenttypes.presentation.group",
	"NTICourseOverViewGroup")
