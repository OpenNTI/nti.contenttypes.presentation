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

from nti.contenttypes.presentation.utils import create_discussionref_from_external

from nti.externalization.externalization import to_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestDiscussion(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_discussion(self):
		path = os.path.join(os.path.dirname(__file__), 'discussion.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		discussion = create_discussionref_from_external(source)
		assert_that(discussion, has_property('label', is_(u'')))
		assert_that(discussion, has_property('title', is_(u'11.6 Perspectives')))
		assert_that(discussion, has_property('icon', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/8c9c6e901a7884087d71ccf46941ad258121abce/fd35e23767020999111e1f49239199b4c5eff23e.jpg")))
		assert_that(discussion, has_property('mimeType', is_(u"application/vnd.nextthought.discussionref")))
		assert_that(discussion, has_property('target', is_(u"tag:nextthought.com,2011-10:LSTD_1153-Topic:EnrolledCourseRoot-Open_Discussions.11_6_Perspectives")))
		assert_that(discussion, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:LSTD_1153-DiscussionRef:EnrolledCourseRoot-Open_Discussions.11_6_Perspectives")))
		
		ext_obj = to_external_object(discussion, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
