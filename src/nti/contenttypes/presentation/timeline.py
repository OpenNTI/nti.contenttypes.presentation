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

from nti.common.property import alias

from nti.contenttypes.presentation import NTI_TIMELINE
from nti.contenttypes.presentation import NTI_TIMELIME_REF

from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTITimelineRef

from nti.schema.eqhash import EqHash 

from nti.schema.fieldproperty import createDirectFieldProperties

@total_ordering
@EqHash('ntiid')
@interface.implementer(INTITimeline)
class NTITimeLine(PersistentPresentationAsset):
	createDirectFieldProperties(INTITimeline)

	__external_class_name__ = u"Timeline"
	mime_type = mimeType = u'application/vnd.nextthought.ntitimeline'

	desc = alias('description')

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(NTI_TIMELINE)
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

@interface.implementer(INTITimelineRef)
class NTITimeLineRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTITimelineRef)

	__external_class_name__ = u"TimelineRef"
	mime_type = mimeType = u'application/vnd.nextthought.ntitimelineref'

	__name__ = alias('ntiid')

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(NTI_TIMELIME_REF)
		return self.ntiid
