#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.common.property import alias

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTITimeline

@interface.implementer(INTITimeline)
@EqHash('ntiid')
class NTITimeLine(PersistentPresentationAsset):
	createDirectFieldProperties(INTITimeline)

	__external_class_name__ = u"Timeline"
	mime_type = mimeType = u'application/vnd.nextthought.timeline'

	desc = alias('description')
