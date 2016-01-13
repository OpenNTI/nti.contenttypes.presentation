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

from nti.common.property import alias

from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import INTITimeline

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

@total_ordering
@EqHash('ntiid')
@interface.implementer(INTITimeline)
class NTITimeLine(PersistentPresentationAsset):
	createDirectFieldProperties(INTITimeline)

	__external_class_name__ = u"Timeline"
	mime_type = mimeType = u'application/vnd.nextthought.ntitimeline'

	desc = alias('description')

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
