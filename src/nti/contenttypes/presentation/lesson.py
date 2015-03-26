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

from nti.common.property import alias
from nti.common.property import readproperty

from nti.ntiids.ntiids import make_ntiid

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTILessonOverview
from .interfaces import INTICourseOverviewGroup
from .interfaces import INTICourseOverviewSpacer

from . import NTI_COURSE_OVERVIEW_GROUP

@interface.implementer(INTICourseOverviewSpacer)
class NTICourseOverViewSpacer(PersistentPresentationAsset):
	createDirectFieldProperties(INTICourseOverviewSpacer)
	
	__external_class_name__ = u"CourseOverviewSpacer"
	mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewspacer"

@interface.implementer(INTICourseOverviewGroup)
@EqHash('ntiid')
class NTICourseOverViewGroup(PersistentPresentationAsset):
	createDirectFieldProperties(INTICourseOverviewGroup)

	__external_class_name__ = u"CourseOverviewGroup"
	mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewgroup"
	
	color = alias('accentColor')
	items = alias('Items')

	@readproperty
	def ntiid(self):
		result = make_ntiid(provider='NTI',
							nttype=NTI_COURSE_OVERVIEW_GROUP,
							specific=md5(str(uuid.uuid4())).hexdigest() )
		return result
	
	def __getitem__(self, index):
		return self.items[index]
	
	def __len__(self):
		return len(self.items or ())

	def __iter__(self):
		return iter(self.items or ())
	
	def sublocations(self):
		for item in self.items or ():
			yield item

@interface.implementer(INTILessonOverview)
@EqHash('ntiid')
class NTILessonOverView(PersistentPresentationAsset):
	createDirectFieldProperties(INTILessonOverview)

	__external_class_name__ = u"LessonOverView"
	mime_type = mimeType = u"application/vnd.nextthought.ntilessonoverview"
	
	items = alias('Items')

	def __getitem__(self, index):
		return self.items[index]
	
	def __len__(self):
		return len(self.items or ())

	def __iter__(self):
		return iter(self.items or ())
	
	def sublocations(self):
		for item in self.items or ():
			yield item
