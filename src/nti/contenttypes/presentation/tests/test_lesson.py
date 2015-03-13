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
from hamcrest import has_length
from hamcrest import has_entries
from hamcrest import assert_that
from hamcrest import has_property

import os
import copy
import unittest
import simplejson

from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIRelatedWork
from nti.contenttypes.presentation.interfaces import INTIAssignmentRef
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup

from nti.contenttypes.presentation.utils import create_object_from_external

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.externalization import to_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

ITEMS = StandardExternalFields.ITEMS

class TestLesson(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_nticourseoverviewgroup(self):
		path = os.path.join(os.path.dirname(__file__), 'nticourseoverviewgroup.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)

		group = create_object_from_external(source)
		assert_that(group, has_property('ntiid', is_not(none())))
		assert_that(group, has_property('color', is_(u'f11824e')))
		assert_that(group, has_property('title', is_(u'Required Resources')))
		assert_that(group, has_property('Items', has_length(2)))
		assert_that(group, has_property('mimeType', is_(u"application/vnd.nextthought.nticourseoverviewgroup")))
		
		assert_that(group, has_length(2))
		assert_that(list(group), has_length(2))
		assert_that(group[0], validly_provides(INTIRelatedWork))
		assert_that(group[1], verifiably_provides(INTIAssignmentRef))
		
		ext_obj = to_external_object(group, name="render")
		for k, v in original.items():
			if k != ITEMS:
				assert_that(ext_obj, has_entry(k, is_(v)))
			else:
				for idx, org_item in enumerate(v):
					ext_item = ext_obj[ITEMS][idx]
					assert_that(ext_item, has_entries(**org_item))

	def test_ntilessonoverview(self):
		path = os.path.join(os.path.dirname(__file__), 'ntilessonoverview.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")

		lesson = create_object_from_external(source)
		assert_that(lesson, has_property('ntiid', is_(u'tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.lec:11.06_LESSON')))
		assert_that(lesson, has_property('Items', has_length(4)))
		assert_that(lesson, has_property('mimeType', is_(u"application/vnd.nextthought.ntilessonoverview")))
		
		assert_that(lesson, has_length(4))
		assert_that(list(lesson), has_length(4))
		for item in lesson:
			assert_that(item, validly_provides(INTICourseOverviewGroup))
		
		for item in lesson[1]:
			assert_that(item, validly_provides(INTIAssignmentRef))
			
		for item in lesson[-1]:
			assert_that(item, validly_provides(INTIVideoRef))
	
		ext_obj = to_external_object(lesson, name="render")
		assert_that(ext_obj, has_entry('NTIID', is_(u"tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.lec:11.06_LESSON")))
		assert_that(ext_obj, has_entry('MimeType', is_(u"application/vnd.nextthought.ntilessonoverview")))
		assert_that(ext_obj, has_entry('title', is_(u"11.6 Apply Your Knowledge")))
		assert_that(ext_obj, has_entry('Items', has_length(4)))

		