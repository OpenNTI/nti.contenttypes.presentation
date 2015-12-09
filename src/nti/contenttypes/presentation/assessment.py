#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.common.property import alias

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTIPollRef
from .interfaces import INTISurveyRef
from .interfaces import INTIQuestionRef
from .interfaces import INTIAssignmentRef
from .interfaces import INTIQuestionSetRef

from . import NTI_POLL_REF
from . import NTI_SURVEY_REF
from . import NTI_QUESTION_REF
from . import NTI_ASSIGNMENT_REF
from . import NTI_QUESTION_SET_REF

import zope.deferredimport
zope.deferredimport.initialize()

@EqHash('ntiid')
class NTIAssessmentRef(PersistentPresentationAsset):

	nttype = 'NTIAssessmentRef'
	target_ntiid = alias('target')
	
	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(self.nttype)
		return self.ntiid
	
	@readproperty
	def target(self):
		return self.ntiid

@interface.implementer(INTIAssignmentRef)
class NTIAssignmentRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIAssignmentRef)

	__external_class_name__ = u"AssignmentRef"
	mime_type = mimeType = u"application/vnd.nextthought.assignmentref"

	nttype = NTI_ASSIGNMENT_REF 
	ContainerId = alias('containerId')

@interface.implementer(INTIQuestionSetRef)
class NTIQuestionSetRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionSetRef)

	__external_class_name__ = u"QuestionSetRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionsetref"

	nttype = NTI_QUESTION_SET_REF 
	
zope.deferredimport.deprecated(
	"Import from NTIQuestionSetRef instead",
	NTQuestionSetRef='nti.contenttypes.presentation.assessment:NTIQuestionSetRef')

@interface.implementer(INTIQuestionRef)
class NTIQuestionRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIQuestionRef)

	__external_class_name__ = u"QuestionRef"
	mime_type = mimeType = u"application/vnd.nextthought.questionref"
	
	nttype = NTI_QUESTION_REF 

zope.deferredimport.deprecated(
	"Import from NTIQuestionRef instead",
	NTQuestionRef='nti.contenttypes.presentation.assessment:NTIQuestionRef')

@interface.implementer(INTISurveyRef)
class NTISurveyRef(NTIAssessmentRef):
	createDirectFieldProperties(INTISurveyRef)

	__external_class_name__ = u"SurveyRef"
	mime_type = mimeType = u"application/vnd.nextthought.surveyref"

	nttype = NTI_SURVEY_REF 
	ContainerId = alias('containerId')

@interface.implementer(INTIPollRef)
class NTIPollRef(NTIAssessmentRef):
	createDirectFieldProperties(INTIPollRef)

	__external_class_name__ = u"PollRef"
	mime_type = mimeType = u"application/vnd.nextthought.pollref"
	
	nttype = NTI_POLL_REF 
