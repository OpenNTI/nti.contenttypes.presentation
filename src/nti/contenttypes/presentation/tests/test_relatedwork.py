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

class TestRelatedWork(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_related(self):
		path = os.path.join(os.path.dirname(__file__), 'relatedwork.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		related = factory()
		update_from_external_object(related, source)
		assert_that(related, has_property('creator', is_(u'Steven M. Gillon')))
		assert_that(related, has_property('label', is_(u'The Critical Year: 1968')))
		assert_that(related, has_property('type', is_(u"application/vnd.nextthought.content")))
		assert_that(related, has_property('icon', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/420c90cea830984c7260c255692e6cd794e2b281/fd35e23767020999111e1f49239199b4c5eff23e.jpg")))
		assert_that(related, has_property('desc', is_(u"A look at how the U.S. came to a crossroads in 1968, when faced with the Vietnam War, political partisanship, racial violence, and social upheaval.")))
		assert_that(related, has_property('mimeType', is_(u"application/vnd.nextthought.relatedworkref")))
		assert_that(related, has_property('target', is_(u"tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.reading:12.3_1")))
		assert_that(related, has_property('href', is_(u"tag:nextthought.com,2011-10:OU-HTML-LSTD1153_S_2015_History_United_States_1865_to_Present.reading:12.3_1")))
		assert_that(related, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-RelatedWork-LSTD1153_S_2015_History_United_States_1865_to_Present.relatedwork.relwk:12.3_1_Critical_Year_1968")))
		
		ext_obj = to_external_object(related, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
