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

from nti.externalization.externalization import to_external_object

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestModel(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_ntivideo(self):
		path = os.path.join(os.path.dirname(__file__), 'timeline.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		timeline = factory()
		update_from_external_object(timeline, source)
		assert_that(timeline, has_property('label', is_(u"Heading West")))
		assert_that(timeline, has_property('mimeType', is_(u"application/vnd.nextthought.timeline")))
		assert_that(timeline, has_property('description', is_(u"An overview of key dates and events")))
		assert_that(timeline, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-JSON:Timeline-LSTD1153_S_2015_History_United_States_1865_to_Present.timeline.heading_west")))
		assert_that(timeline, has_property('href', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/d1b15ecbe7e15f47d1927624e23b40509d37f135/90784fa2c5c148922446e05d45ff35f0aee3e69b.json")))
		assert_that(timeline, has_property('icon', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/75d1ec44cd623dfdc373b705523e05259f61c821/fd35e23767020999111e1f49239199b4c5eff23e.jpg")))
		
		ext_obj = to_external_object(timeline, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
