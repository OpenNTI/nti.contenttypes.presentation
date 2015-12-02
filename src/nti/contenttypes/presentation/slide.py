#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from itertools import chain

from zope import interface

from persistent.list import PersistentList

from nti.common.property import alias
from nti.common.property import CachedProperty 

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTISlide
from .interfaces import INTISlideDeck
from .interfaces import INTISlideVideo

@EqHash('ntiid')
@interface.implementer(INTISlide)
class NTISlide(PersistentPresentationAsset):
	createDirectFieldProperties(INTISlide)

	__external_class_name__ = u"Slide"
	mime_type = mimeType = u'application/vnd.nextthought.slide'

	image = alias('slideimage')
	number = alias('slidenumber')
	video = alias('slidevideoid')
	slide_deck = deck = alias('slidedeckid')
	end = video_end = alias('slidevideoend')
	start = video_start = alias('slidevideostart')

@EqHash('ntiid')
@interface.implementer(INTISlideVideo)
class NTISlideVideo(PersistentPresentationAsset):
	createDirectFieldProperties(INTISlideVideo)

	__external_class_name__ = u"NTISlideVideo"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidevideo'

	Creator = alias('creator')
	video = alias('video_ntiid')
	slide_deck = deck = alias('slidedeckid')

@EqHash('ntiid')
@interface.implementer(INTISlideDeck)
class NTISlideDeck(PersistentPresentationAsset):
	createDirectFieldProperties(INTISlideDeck)

	__external_class_name__ = u"NTISlideDeck"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidedeck'

	slides = alias('Slides')
	videos = alias('Videos')
	Creator = alias('creator')
	id = alias('slidedeckid')
	
	@CachedProperty("lastModified")
	def Items(self):
		result = list(chain(self.slides or (), self.videos or ()))
		return result

	def append(self, item):
		if INTISlide.providedBy(item):
			self.slides = PersistentList() if self.slides is None else self.slides
			self.slides.append(item)
		elif INTISlideVideo.providedBy(item):
			self.videos = PersistentList() if self.videos is None else self.videos
			self.videos.append(item)
	add = append
		
	def remove(self, item):
		result = True
		try:
			if INTISlide.providedBy(item) and self.slides:
				self.slides.remove(item)
			elif INTISlideVideo.providedBy(item) and self.videos:
				self.videos.remove(item)
			else:
				result = False
		except ValueError:
			result = False
		return result
