#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_property

import os
import copy
import unittest
import simplejson

from nti.contenttypes.presentation.utils import create_questionref_from_external
from nti.contenttypes.presentation.utils import create_assignmentref_from_external
from nti.contenttypes.presentation.utils import create_questionsetref_from_external

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.externalization import to_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

MIMETYPE = StandardExternalFields.MIMETYPE

class TestAssignment(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_assignment(self):
		path = os.path.join(os.path.dirname(__file__), 'assignment.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
		assert_that(source, has_entry(MIMETYPE, is_('application/vnd.nextthought.assessment.assignment')))
		
		assignment = create_assignmentref_from_external(source)
		assert_that(assignment, has_property('containerId', is_(u'tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.discussions:_the_liberal_hour')))
		assert_that(assignment, has_property('title', is_(u'Discussions: The Liberal Hour')))
		assert_that(assignment, has_property('label', is_(u'Discussions: The Liberal Hour')))
		assert_that(assignment, has_property('target', is_(u"tag:nextthought.com,2011-10:OU-NAQ-LSTD1153_S_2015_History_United_States_1865_to_Present.naq.asg.assignment:11.6_discussions")))
		assert_that(assignment, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NAQ-LSTD1153_S_2015_History_United_States_1865_to_Present.naq.asg.assignment:11.6_discussions")))
		
		ext_obj = to_external_object(assignment, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))

	def test_questionset(self):
		path = os.path.join(os.path.dirname(__file__), 'questionset.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
		assert_that(source, has_entry(MIMETYPE, is_('application/vnd.nextthought.naquestionset')))
		
		questionset = create_questionsetref_from_external(source)
		assert_that(questionset, has_property('question_count', is_(7)))
		assert_that(questionset, has_property('label', is_(u'Janux Course Features Verification Quiz')))
		assert_that(questionset, has_property('target', is_(u"tag:nextthought.com,2011-10:OU-NAQ-CHEM4970_200_F_2014_Chemistry_of_Beer.naq.set.qset:janux_features_verification_quiz")))
		assert_that(questionset, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NAQ-CHEM4970_200_F_2014_Chemistry_of_Beer.naq.set.qset:janux_features_verification_quiz")))
		
		ext_obj = to_external_object(questionset, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))

	def test_question(self):
		path = os.path.join(os.path.dirname(__file__), 'question.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
		assert_that(source, has_entry(MIMETYPE, is_('application/vnd.nextthought.naquestion')))
		
		question = create_questionref_from_external(source)
		assert_that(question, has_property('target', is_(u"tag:nextthought.com,2011-10:OKState-NAQ-OKState_AGEC4990_S_2015_Farm_to_Fork.naq.qid.FootprintQuiz.01")))
		assert_that(question, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OKState-NAQ-OKState_AGEC4990_S_2015_Farm_to_Fork.naq.qid.FootprintQuiz.01")))
		
		ext_obj = to_external_object(question, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))