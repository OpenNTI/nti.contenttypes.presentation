#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
from hamcrest.library.object.haslength import has_length
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

class TestSlide(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_slide(self):
		path = os.path.join(os.path.dirname(__file__), 'slide.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		slide = factory()
		update_from_external_object(slide, source)
		assert_that(slide, has_property('number', is_(11)))
		assert_that(slide, has_property('end', is_(398.0)))
		assert_that(slide, has_property('start', is_(354.0)))
		assert_that(slide, has_property("deck", "tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Insertion_Sort"))
		assert_that(slide, has_property('mimeType', is_(u"application/vnd.nextthought.slide")))
		assert_that(slide, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NTISlide-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Insertion_Sort_slide_11")))
		assert_that(slide, has_property('image', is_(u"resources/CS1323_S_2015_Intro_to_Computer_Programming/e3573369b10854aea33ccaf31260b51ff1384069/fd35e23767020999111e1f49239199b4c5eff23e.png")))
	
		ext_obj = to_external_object(slide, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))

	def test_ntislidevideo(self):
		path = os.path.join(os.path.dirname(__file__), 'ntislidevideo.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		slide = factory()
		update_from_external_object(slide, source)
		assert_that(slide, has_property('thumbnail', is_("//www.kaltura.com/p/1500101/thumbnail/entry_id/0_06h42bu6/width/640/")))
		assert_that(slide, has_property('creator', is_("Deborah Trytten")))
		assert_that(slide, has_property('title', is_("Install Software on Macintosh")))
		assert_that(slide, has_property("deck", "tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac"))
		assert_that(slide, has_property('mimeType', is_(u"application/vnd.nextthought.ntislidevideo")))
		assert_that(slide, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NTISlideVideo-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac_video")))
		assert_that(slide, has_property('video', is_(u"tag:nextthought.com,2011-10:OU-NTIVideo-CS1323_S_2015_Intro_to_Computer_Programming.ntivideo.video_01.01.02_Mac")))
	
		ext_obj = to_external_object(slide, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))

	def test_ntislidedeck(self):
		path = os.path.join(os.path.dirname(__file__), 'ntislidedeck.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			
		factory = find_factory_for(source)
		assert_that(factory, is_not(none()))
		slide = factory()
		update_from_external_object(slide, source)
		assert_that(slide, has_property('creator', is_("Deborah Trytten")))
		assert_that(slide, has_property('title', is_("Install Software on a Macintosh")))
		assert_that(slide, has_property("id",    is_(u"tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac")))
		assert_that(slide, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac")))
		assert_that(slide, has_property('mimeType', is_(u"application/vnd.nextthought.ntislidedeck")))
		assert_that(slide, has_property('videos', has_length(1)))
		assert_that(slide, has_property('slides', has_length(19)))

		ext_obj = to_external_object(slide, name="render")
		assert_that(ext_obj, has_entry('creator', is_("Deborah Trytten")))
		assert_that(ext_obj, has_entry('title', is_("Install Software on a Macintosh")))
		assert_that(ext_obj, has_entry('MimeType', is_(u"application/vnd.nextthought.ntislidedeck")))
		assert_that(ext_obj, has_entry('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac")))
		assert_that(ext_obj, has_entry('slidedeckid', is_(u"tag:nextthought.com,2011-10:OU-NTISlideDeck-CS1323_S_2015_Intro_to_Computer_Programming.nsd.pres:Install_Mac")))
		assert_that(ext_obj, has_entry('Videos', has_length(1)))
		assert_that(ext_obj, has_entry('Slides', has_length(19)))
		