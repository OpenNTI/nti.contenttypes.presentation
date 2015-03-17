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

from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIQuestionSetRef

@interface.implementer(IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTIAssessmentRef(	SchemaConfigured,
						PersistentPropertyHolder,
				 		Contained):
	
	target_ntiid = alias('target')
		
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
		
@interface.implementer(INTIAssignmentRef)
class NTIAssignmentRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIAssignmentRef)

	__external_class_name__ = u"AssignmentRef"
	mime_type = mimeType = u"application/vnd.nextthought.assignmentref"
	
	ContainerId = alias('containerId')

@interface.implementer(INTIQuestionSetRef)
class NTQuestionSetRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionSetRef)

	__external_class_name__ = u"QuestionSetRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionsetref"

@interface.implementer(INTIQuestionRef)
class NTQuestionRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionRef)

	__external_class_name__ = u"QuestionRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionref"
