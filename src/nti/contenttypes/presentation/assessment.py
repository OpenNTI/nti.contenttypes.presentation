#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.contenttypes.presentation import NTI_POLL_REF
from nti.contenttypes.presentation import NTI_SURVEY_REF
from nti.contenttypes.presentation import NTI_QUESTION_REF
from nti.contenttypes.presentation import NTI_ASSIGNMENT_REF
from nti.contenttypes.presentation import NTI_QUESTION_SET_REF

from nti.contenttypes.presentation.interfaces import INTIPollRef
from nti.contenttypes.presentation.interfaces import INTISurveyRef
from nti.contenttypes.presentation.interfaces import INTIQuestionRef
from nti.contenttypes.presentation.interfaces import INTIAssignmentRef
from nti.contenttypes.presentation.interfaces import INTIQuestionSetRef

from nti.contenttypes.presentation.mixins import PersistentPresentationAsset

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties

logger = __import__('logging').getLogger(__name__)


@total_ordering
class NTIAssessmentRef(PersistentPresentationAsset):

    nttype = u'NTIAssessmentRef'
    target_ntiid = alias('target')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(self.nttype)
        return self.ntiid

    @readproperty
    def target(self):
        return self.ntiid

    def __lt__(self, other):
        try:
            return (self.mimeType, self.label) < (other.mimeType, other.label)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.label) > (other.mimeType, other.label)
        except AttributeError:  # pragma: no cover
            return NotImplemented


@interface.implementer(INTIAssignmentRef)
class NTIAssignmentRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIAssignmentRef)

    __external_class_name__ = "AssignmentRef"
    mime_type = mimeType = "application/vnd.nextthought.assignmentref"

    nttype = NTI_ASSIGNMENT_REF
    ContainerId = alias('containerId')

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented


@interface.implementer(INTIQuestionSetRef)
class NTIQuestionSetRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIQuestionSetRef)

    __external_class_name__ = "QuestionSetRef"
    mime_type = mimeType = "application/vnd.nextthought.questionsetref"

    nttype = NTI_QUESTION_SET_REF


@interface.implementer(INTIQuestionRef)
class NTIQuestionRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIQuestionRef)

    __external_class_name__ = "QuestionRef"
    mime_type = mimeType = "application/vnd.nextthought.questionref"

    nttype = NTI_QUESTION_REF


@interface.implementer(INTISurveyRef)
class NTISurveyRef(NTIAssessmentRef):
    createDirectFieldProperties(INTISurveyRef)

    __external_class_name__ = "SurveyRef"
    mime_type = mimeType = "application/vnd.nextthought.surveyref"

    nttype = NTI_SURVEY_REF
    ContainerId = alias('containerId')


@interface.implementer(INTIPollRef)
class NTIPollRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIPollRef)

    __external_class_name__ = "PollRef"
    mime_type = mimeType = "application/vnd.nextthought.pollref"

    nttype = NTI_POLL_REF


import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from NTIQuestionRef instead",
    NTQuestionRef='nti.contenttypes.presentation.assessment:NTIQuestionRef',
    NTQuestionSetRef='nti.contenttypes.presentation.assessment:NTIQuestionSetRef')
