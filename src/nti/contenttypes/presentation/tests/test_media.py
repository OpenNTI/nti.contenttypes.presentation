#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property

import os
import copy
import unittest
import simplejson

from nti.contenttypes.presentation.utils import create_ntiaudio_from_external
from nti.contenttypes.presentation.utils import create_ntivideo_from_external

from nti.externalization.externalization import to_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

class TestMedia(unittest.TestCase):

	layer = SharedConfiguringTestLayer

	def test_ntivideo(self):
		path = os.path.join(os.path.dirname(__file__), 'ntivideo.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		ntivideo = create_ntivideo_from_external(source)
		assert_that(ntivideo, has_property('creator', is_(u'OU')))
		assert_that(ntivideo, has_property('title', is_(u"Andrew Johnson")))
		assert_that(ntivideo, has_property('mimeType', is_(u"application/vnd.nextthought.ntivideo")))
		assert_that(ntivideo, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:OU-NTIVideo-LSTD1153_S_2015_History_United_States_1865_to_Present.ntivideo.video_Andrew_Johnson")))
		
		assert_that(ntivideo, has_property('sources', has_length(1)))
		source = ntivideo.sources[0]
		
		assert_that(source, has_property('service', is_(u"kaltura")))
		assert_that(source, has_property('source', is_(["1500101:0_hwfe5zjr"])))
		assert_that(source, has_property('poster', is_(u"//www.kaltura.com/p/1500101/thumbnail/entry_id/0_hwfe5zjr/width/1280/")))
		assert_that(source, has_property('height', is_(480)))
		assert_that(source, has_property('width', is_(640)))
		assert_that(source, has_property('type', is_(["video/kaltura"])))
		assert_that(source, has_property('thumbnail', is_("//www.kaltura.com/p/1500101/thumbnail/entry_id/0_hwfe5zjr/width/640/")))
		
		assert_that(ntivideo, has_property('transcripts', has_length(1)))
		transcript = ntivideo.transcripts[0]
		assert_that(transcript, has_property('srcjsonp', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/cd0332efcd704487fab382b76fdc0523fb2dad7e/9b3fe7737c9828ea6a552664d89b26bc8de8a15e.jsonp")))
		assert_that(transcript, has_property('src', is_(u"resources/LSTD1153_S_2015_History_United_States_1865_to_Present/cd0332efcd704487fab382b76fdc0523fb2dad7e/90784fa2c5c148922446e05d45ff35f0aee3e69b.vtt")))
		assert_that(transcript, has_property('type', is_(u"text/vtt")))
		assert_that(transcript, has_property('lang', is_(u"en")))
		assert_that(transcript, has_property('purpose', is_(u"normal")))

		ext_obj = to_external_object(ntivideo, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
			
	def test_ntiaudio(self):
		path = os.path.join(os.path.dirname(__file__), 'ntiaudio.json')
		with open(path, "r") as fp:
			source = simplejson.load(fp, encoding="UTF-8")
			original = copy.deepcopy(source)
			
		ntiaudio = create_ntiaudio_from_external(source)
		assert_that(ntiaudio, has_property('creator', is_(u'Alibra')))
		assert_that(ntiaudio, has_property('title', is_(u"audio")))
		assert_that(ntiaudio, has_property('mimeType', is_(u"application/vnd.nextthought.ntiaudio")))
		assert_that(ntiaudio, has_property('ntiid', is_(u"tag:nextthought.com,2011-10:Alibra-NTIAudio-Alibra_Unit7.ntiaudio.audio_90how")))
		
		assert_that(ntiaudio, has_property('sources', has_length(1)))
		source = ntiaudio.sources[0]
		
		assert_that(source, has_property('service', is_(u"html5")))
		assert_that(source, has_property('source', has_length(2)))
		assert_that(source, has_property('type', has_length(2)))
		assert_that(source, has_property('thumbnail', is_("//s3.amazonaws.com/media.nextthought.com/Alibra/Unit07/90+how-thumb.jpg")))
		
		ext_obj = to_external_object(ntiaudio, name="render")
		for k, v in original.items():
			assert_that(ext_obj, has_entry(k, is_(v)))
