#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import sys
import inspect
import unittest

from zope import interface

from nti.contenttypes.presentation import iface_of_asset
from nti.contenttypes.presentation import PACKAGE_CONTAINER_INTERFACES
from nti.contenttypes.presentation import GROUP_OVERVIEWABLE_INTERFACES
from nti.contenttypes.presentation import ALL_PRESENTATION_ASSETS_INTERFACES

from nti.contenttypes.presentation.group import NTICourseOverViewGroup

from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup

from nti.contenttypes.presentation.lesson import NTILessonOverView

from nti.schema.interfaces import find_most_derived_interface

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestModule(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_ifaces(self):
		assert_that(GROUP_OVERVIEWABLE_INTERFACES, is_not(none()))
		assert_that(GROUP_OVERVIEWABLE_INTERFACES, has_length(14))

		assert_that(ALL_PRESENTATION_ASSETS_INTERFACES, is_not(none()))
		assert_that(ALL_PRESENTATION_ASSETS_INTERFACES, has_length(20))

		assert_that(PACKAGE_CONTAINER_INTERFACES, has_length(7))

	def test_asset_ifaces(self):
		class Foo(object):
			pass
		for iface in ALL_PRESENTATION_ASSETS_INTERFACES:
			obj = Foo()
			interface.alsoProvides(obj, iface)
			provided = find_most_derived_interface(obj, IPresentationAsset)
			assert_that(iface_of_asset(obj), is_(provided))

	def test_group(self):
		group = NTICourseOverViewGroup()
		assert_that(group, validly_provides(INTICourseOverviewGroup))
		assert_that(group, verifiably_provides(INTICourseOverviewGroup))

	def test_lesson(self):
		lesson = NTILessonOverView()
		assert_that(lesson, validly_provides(INTILessonOverview))
		assert_that(lesson, verifiably_provides(INTILessonOverview))

	def test_factories(self):

		def _ext_mime_type_predicate(item):
			result = bool(type(item) == interface.interface.InterfaceClass) \
					and item.queryTaggedValue('_ext_mime_type')
			return result

		module = sys.modules[INTILessonOverview.__module__]
		members = list(inspect.getmembers(module, _ext_mime_type_predicate))
		assert_that(members, has_length(33))
