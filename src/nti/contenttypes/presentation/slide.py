#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.mimetype.interfaces import IContentTypeAware

from nti.common.property import alias

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentMixin

from .interfaces import INTISlide
from .interfaces import INTISlideDeck
from .interfaces import INTISlideVideo

@interface.implementer(INTISlide, IContentTypeAware)
@EqHash('ntiid')
class NTISlide(PersistentMixin):
	createDirectFieldProperties(INTISlide)

	__external_class_name__ = u"Slide"
	mime_type = mimeType = u'application/vnd.nextthought.slide'

	image = alias('slideimage')
	number = alias('slidenumber')
	video = alias('slidevideoid')
	slide_deck = deck = alias('slidedeckid')
	end = video_end = alias('slidevideoend')
	start = video_start = alias('slidevideostart')

@interface.implementer(INTISlideVideo, IContentTypeAware)
@EqHash('ntiid')
class NTISlideVideo(PersistentMixin):
	createDirectFieldProperties(INTISlideVideo)

	__external_class_name__ = u"NTISlideVideo"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidevideo'

	Creator = alias('creator')
	video = alias('video_ntiid')
	slide_deck = deck = alias('slidedeckid')

@interface.implementer(INTISlideDeck, IContentTypeAware)
@EqHash('ntiid')
class NTISlideDeck(PersistentMixin):
	createDirectFieldProperties(INTISlideDeck)

	__external_class_name__ = u"NTISlideDeck"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidedeck'

	slides = alias('Slides')
	videos = alias('Videos')
	Creator = alias('creator')
	id = alias('slidedeckid')
