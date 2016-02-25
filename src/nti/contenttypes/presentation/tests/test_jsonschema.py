#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
from nti.contenttypes.presentation.group import NTICourseOverViewGroup
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
from nti.contenttypes.presentation import ACCEPTS

from nti.contenttypes.presentation.discussion import NTIDiscussionRef

from nti.contenttypes.presentation.media import NTIVideoRef
from nti.contenttypes.presentation.media import NTIMediaRoll
from nti.contenttypes.presentation.media import NTIVideoRoll

from nti.contenttypes.presentation.relatedwork import NTIRelatedWorkRef

from nti.contenttypes.presentation.slide import NTISlide
from nti.contenttypes.presentation.slide import NTISlideDeck
from nti.contenttypes.presentation.slide import NTISlideVideo

from nti.contenttypes.presentation.timeline import NTITimeLine

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestJsonSchema(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_relatedwork(self):
		a = NTIRelatedWorkRef()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(10))
		for field in ('href', 'icon'):
			assert_that(schema, has_entry(field, has_entry('type', 'Variant')))
			assert_that(schema, has_entry(field, has_entry('name', is_(field))))
			assert_that(schema, has_entry(field, has_entry('base_type', [u'string', 'namedfile'])))

		assert_that(schema, has_entry('byline', has_entry('base_type', is_('string'))))
		assert_that(schema, has_entry('target', has_entry('min_length', is_(0))))
		assert_that(schema, has_entry('section', has_entry('min_length', is_(0))))
		assert_that(schema, has_entry('visibility',
									  has_entries('base_type', 'string',
												  'choices', has_length(5))))

	def test_timeline(self):
		a = NTITimeLine()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(6))
		for field in ('href', 'icon'):
			assert_that(schema, has_entry(field, has_entry('type', 'Variant')))
			assert_that(schema, has_entry(field, has_entry('name', is_(field))))
			assert_that(schema, has_entry(field, has_entry('base_type', [u'string', 'namedfile'])))
			
	def test_slide(self):
		a = NTISlide()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(7))
		assert_that(schema, has_entry('slideimage', has_entry('type', 'Variant')))
		assert_that(schema, has_entry('slidenumber', has_entry('type', 'int')))
		assert_that(schema, has_entry('slidenumber', has_entry('base_type', 'int')))
		assert_that(schema, has_entry('slidevideostart', has_entry('type', 'Number')))
		assert_that(schema, has_entry('slidevideostart', has_entry('base_type', 'float')))
		assert_that(schema, has_entry('slideimage', has_entry('base_type', [u'string', 'namedfile'])))
		
	def test_slidevideo(self):
		a = NTISlideVideo()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(7))
		
	def test_slidedeck(self):
		a = NTISlideDeck()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		fields = schema[FIELDS]
		assert_that(fields, has_length(7))
		assert_that(fields, has_entry('Slides', has_entry('type', 'List')))
		assert_that(fields, has_entry('Slides', has_entry('base_type', 'application/vnd.nextthought.slide')))
		assert_that(fields, has_entry('Videos', has_entry('type', 'List')))
		assert_that(fields, has_entry('Videos', has_entry('base_type', 'application/vnd.nextthought.ntislidevideo')))
		
		assert_that(schema, has_key(ACCEPTS))
		accepts = schema[ACCEPTS]
		assert_that(accepts, has_length(2))
		assert_that(accepts, has_key('application/vnd.nextthought.slide'))
		assert_that(accepts, has_key('application/vnd.nextthought.ntislidevideo'))

	def test_discussionref(self):
		a = NTIDiscussionRef()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(6))
		assert_that(schema, has_entry('icon', has_entry('base_type', [u'string', 'namedfile'])))
		
	def test_videoref(self):
		a = NTIVideoRef()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		schema = schema[FIELDS]
		assert_that(schema, has_length(5))
		assert_that(schema, has_entry('target', has_entry('min_length', is_(0))))
		assert_that(schema, has_entry('visibility',
									  has_entries('base_type', 'string',
												  'choices', has_length(5))))

	def test_mediaroll(self):
		a = NTIMediaRoll()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		fields = schema[FIELDS]
		assert_that(fields, has_length(3))
		assert_that(fields, has_entry('Items', has_entry('base_type', 
														 [u'application/vnd.nextthought.ntiaudioref', 
														  u'application/vnd.nextthought.ntivideoref'])))
		assert_that(schema, has_key(ACCEPTS))
		accepts = schema[ACCEPTS]
		assert_that(accepts, has_length(2))

	def test_videoroll(self):
		a = NTIVideoRoll()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		fields = schema[FIELDS]
		assert_that(fields, has_length(3))
		assert_that(fields, has_entry('visibility',
									  has_entries('base_type', 'string',
												  'choices', has_length(5))))
		assert_that(fields, has_entry('Items', has_entry('base_type',
														 u'application/vnd.nextthought.ntivideoref')))
		assert_that(schema, has_key(ACCEPTS))
		accepts = schema[ACCEPTS]
		assert_that(accepts, has_length(1))

	def test_overviewgroup(self):
		a = NTICourseOverViewGroup()
		schema = a.schema()
		assert_that(schema, has_key(FIELDS))
		fields = schema[FIELDS]
		assert_that(fields, has_length(4))
		assert_that(fields, has_entry('Items', has_entry('base_type', has_length(14))))
		assert_that(schema, has_key(ACCEPTS))
		accepts = schema[ACCEPTS]
		assert_that(accepts, has_length(14))
