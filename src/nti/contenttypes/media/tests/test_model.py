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

import os
import unittest
import simplejson

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.contenttypes.media.tests import SharedConfiguringTestLayer

class TestModel(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_internalize(self):
		path = os.path.join(os.path.dirname(__file__), 'ntivideo.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		ntivideo = factory()
		update_from_external_object(ntivideo, source)
		assert_that(ntivideo, has_property('creator', is_(u'OU')))
