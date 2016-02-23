#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_key
from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_entries

import unittest

from nti.contenttypes.presentation import FIELDS

from nti.contenttypes.presentation.relatedwork import NTIRelatedWorkRef

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestJsonSchema(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_relatedwork(self):
		a = NTIRelatedWorkRef()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(12))
		for field in ('href', 'icon'):
			assert_that(schema, has_entry(field, has_entry('type', 'Variant')))
			assert_that(schema, has_entry(field, has_entry('name', is_(field))))
			assert_that(schema, has_entry(field, has_entry('base_type', [u'string', 'namedfile'])))

		assert_that(schema, has_entry('target', has_entry('min_length', is_(0))))
		assert_that(schema, has_entry('section', has_entry('min_length', is_(0))))
		assert_that(schema, has_entry('visibility',
									  has_entries('base_type', 'string',
												  'choices', has_length(5))))
