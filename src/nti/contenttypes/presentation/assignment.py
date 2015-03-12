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

from .interfaces import INTIAssignmentRef

@interface.implementer(INTIAssignmentRef, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTIAssignmentRef(	SchemaConfigured,
						PersistentPropertyHolder,
				 		Contained):
	createDirectFieldProperties(INTIAssignmentRef)

	__external_class_name__ = u"AssignmentRef"
	mime_type = mimeType = u"application/vnd.nextthought.assignmentref"
	
	target_ntiid = alias('target')
	ContainerId = alias('containerId')
		
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
