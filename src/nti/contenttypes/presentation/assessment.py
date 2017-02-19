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

from nti.contenttypes.presentation import NTI_POLL_REF
from nti.contenttypes.presentation import NTI_SURVEY_REF
from nti.contenttypes.presentation import NTI_QUESTION_REF
from nti.contenttypes.presentation import NTI_ASSIGNMENT_REF
from nti.contenttypes.presentation import NTI_QUESTION_SET_REF

from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import INTIPollRef
from nti.contenttypes.presentation.interfaces import INTISurveyRef
from nti.contenttypes.presentation.interfaces import INTIQuestionRef
from nti.contenttypes.presentation.interfaces import INTIAssignmentRef
from nti.contenttypes.presentation.interfaces import INTIQuestionSetRef

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties


@total_ordering
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


@interface.implementer(INTIAssignmentRef)
class NTIAssignmentRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIAssignmentRef)

    __external_class_name__ = u"AssignmentRef"
    mime_type = mimeType = u"application/vnd.nextthought.assignmentref"

    nttype = NTI_ASSIGNMENT_REF
    ContainerId = alias('containerId')

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented


@interface.implementer(INTIQuestionSetRef)
class NTIQuestionSetRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIQuestionSetRef)

    __external_class_name__ = u"QuestionSetRef"
    mime_type = mimeType = u"application/vnd.nextthought.questionsetref"

    nttype = NTI_QUESTION_SET_REF


@interface.implementer(INTIQuestionRef)
class NTIQuestionRef(NTIAssessmentRef):
    createDirectFieldProperties(INTIQuestionRef)

    __external_class_name__ = u"QuestionRef"
    mime_type = mimeType = u"application/vnd.nextthought.questionref"

    nttype = NTI_QUESTION_REF


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

import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from NTIQuestionRef instead",
    NTQuestionRef='nti.contenttypes.presentation.assessment:NTIQuestionRef',
    NTQuestionSetRef='nti.contenttypes.presentation.assessment:NTIQuestionSetRef')
