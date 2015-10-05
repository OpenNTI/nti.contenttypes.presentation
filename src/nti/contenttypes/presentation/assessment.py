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

from .interfaces import INTIPollRef
from .interfaces import INTISurveyRef
from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIQuestionSetRef

from ._base import PersistentPresentationAsset

import zope.deferredimport
zope.deferredimport.initialize()

@EqHash('ntiid')
class NTIAssessmentRef(PersistentPresentationAsset):
	target_ntiid = alias('target')

@interface.implementer(INTIAssignmentRef)
class NTIAssignmentRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIAssignmentRef)

	__external_class_name__ = u"AssignmentRef"
	mime_type = mimeType = u"application/vnd.nextthought.assignmentref"

	ContainerId = alias('containerId')

@interface.implementer(INTIQuestionSetRef)
class NTIQuestionSetRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionSetRef)

	__external_class_name__ = u"QuestionSetRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionsetref"

zope.deferredimport.deprecated(
	"Import from NTIQuestionSetRef instead",
	NTQuestionSetRef='nti.contenttypes.presentation.assessment:NTIQuestionSetRef')

@interface.implementer(INTIQuestionRef)
class NTIQuestionRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionRef)

	__external_class_name__ = u"QuestionRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionref"

zope.deferredimport.deprecated(
	"Import from NTIQuestionRef instead",
	NTQuestionRef='nti.contenttypes.presentation.assessment:NTIQuestionRef')

@interface.implementer(INTISurveyRef)
class NTISurveyRef(NTIAssessmentRef):
	createDirectFieldProperties(INTISurveyRef)

	__external_class_name__ = u"SurveyRef"
	mime_type = mimeType = u"application/vnd.nextthought.surveyref"

	ContainerId = alias('containerId')

@interface.implementer(INTIPollRef)
class NTIPollRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIPollRef)

	__external_class_name__ = u"PollRef"
	mime_type = mimeType = u"application/vnd.nextthought.pollref"
