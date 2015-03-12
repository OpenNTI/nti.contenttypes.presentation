#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.container.contained import Contained

from zope.mimetype.interfaces import IContentTypeAware

from nti.common.property import alias

from nti.externalization.representation import WithRepr

from nti.schema.schema import EqHash 
from nti.schema.field import SchemaConfigured
from nti.schema.fieldproperty import createDirectFieldProperties

from nti.zodb.persistentproperty import PersistentPropertyHolder

from .interfaces import INTIRelatedWork

@interface.implementer(INTIRelatedWork, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTIRelatedWork(SchemaConfigured,
				  	 PersistentPropertyHolder,
				  	 Contained):
	createDirectFieldProperties(INTIRelatedWork)

	__external_class_name__ = u"RelatedWork"
	mime_type = mimeType = u'application/vnd.nextthought.relatedworkref'

	Creator = alias('creator')
	desc = alias('description')
	target_ntiid =  alias('target')
	
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
