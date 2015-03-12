#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_property

import os
import copy
import unittest
import simplejson

from nti.contenttypes.presentation.assignment import NTIAssignmentRef

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.externalization import to_external_object

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

MIMETYPE = StandardExternalFields.MIMETYPE

class TestAssignment(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_related(self):
		path = os.path.join(os.path.dirname(__file__), 'assignment.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		assert_that(source, has_entry(MIMETYPE, is_('application/vnd.nextthought.assessment.assignment')))
		source[MIMETYPE] = NTIAssignmentRef.mime_type # to factory can be found
		
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		assignment = factory()
		update_from_external_object(assignment, source)
		assert_that(assignment, has_property('containerId', is_(u'tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.discussions:_the_liberal_hour')))
		assert_that(assignment, has_property('title', is_(u'Discussions: The Liberal Hour')))
		assert_that(assignment, has_property('label', is_(u'Discussions: The Liberal Hour')))
		assert_that(assignment, has_property('target', is_(u"tag:nextthought.com,2011-10:OU-NAQ-LSTD1153_S_2015_History_United_States_1865_to_Present.naq.asg.assignment:11.6_discussions")))
		assert_that(assignment, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NAQ-LSTD1153_S_2015_History_United_States_1865_to_Present.naq.asg.assignment:11.6_discussions")))
		
		ext_obj = to_external_object(assignment, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
