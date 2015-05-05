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

from nti.wref.interfaces import IWeakRef

from ._base import PersistentPresentationAsset

from .interfaces import INTICourseOverviewGroup

from . import NTI_COURSE_OVERVIEW_GROUP

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
		item = self.items[index]
		item = item() if IWeakRef.providedBy(item) else item
		return item
	
	def __setitem__(self, index, item):
		self.items[index] = item
	
	def __len__(self):
		result = len(self.items)
		return result

	def __iter__(self):
		for item in self.items or ():
			item = item() if IWeakRef.providedBy(item) else item
			yield item
	
	def sublocations(self):
		for item in self:
			yield item
