#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from .interfaces import INTIDiscussion

from ._base import PersistentPresentationAsset

@interface.implementer(INTIDiscussion)
@EqHash('ntiid')
class NTIDiscussion(PersistentPresentationAsset):
	createDirectFieldProperties(INTIDiscussion)

	__external_class_name__ = u"Discussion"
	mime_type = mimeType = u'application/vnd.nextthought.discussionref'
