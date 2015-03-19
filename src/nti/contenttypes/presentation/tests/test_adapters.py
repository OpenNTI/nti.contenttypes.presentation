#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from nti.contenttypes.presentation.discussion import NTIDiscussion
from nti.contenttypes.presentation.discussion import make_discussionref_ntiid

from nti.contenttypes.presentation.interfaces import INTIDiscussionRef

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestAdapters(unittest.TestCase):

	layer = SharedConfiguringTestLayer
	
	def test_discussion(self):
		ntiid = u"tag:nextthought.com,2011-10:LSTD_1153-Topic:EnrolledCourseRoot-Open_Discussions.11_6_Perspectives"
		d = NTIDiscussion(label=u"",
						  title=u"11.6 Perspectives",
						  icon=u"resources/LSTD.jpg",
						  ntiid=ntiid)
		ref = INTIDiscussionRef(d, None)
		assert_that(ref, is_not(none()))
		assert_that(ref, has_property("label", is_("")))
		assert_that(ref, has_property("icon", is_(u"resources/LSTD.jpg")))
		assert_that(ref, has_property("title", is_(u"11.6 Perspectives")))
		assert_that(ref, has_property("target", is_(ntiid)))
		assert_that(ref, has_property("ntiid", is_(make_discussionref_ntiid(ntiid))))
