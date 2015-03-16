#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.contenttypes.presentation import GROUP_OVERVIEWABLE_INTERFACES

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestModule(unittest.TestCase):

	layer = SharedConfiguringTestLayer
	
	def test_ifaces(self):
		assert_that(GROUP_OVERVIEWABLE_INTERFACES, is_not(none()))
		assert_that(GROUP_OVERVIEWABLE_INTERFACES, has_length(7))
