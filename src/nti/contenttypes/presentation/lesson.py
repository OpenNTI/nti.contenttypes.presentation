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

from nti.ntiids.ntiids import make_ntiid

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewSpacer

from . import NTI_COURSE_OVERVIEW_SPACER

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
class NTILessonOverView(PersistentPresentationAsset):
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

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
	"moved to nti.contenttypes.presentation.group",
	"nti.contenttypes.presentation.group",
	"NTICourseOverViewGroup")
