#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.container.contained import Contained

from zope.mimetype.interfaces import IContentTypeAware

from nti.common.property import alias

from nti.externalization.representation import WithRepr

from nti.schema.schema import EqHash 
from nti.schema.field import SchemaConfigured
from nti.schema.fieldproperty import createDirectFieldProperties

from nti.zodb.persistentproperty import PersistentPropertyHolder

from .interfaces import INTISlide
from .interfaces import INTISlideDeck
from .interfaces import INTISlideVideo

@interface.implementer(INTISlide, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTISlide(	SchemaConfigured,
				PersistentPropertyHolder,
				Contained):
	createDirectFieldProperties(INTISlide)

	__external_class_name__ = u"Slide"
	mime_type = mimeType = u'application/vnd.nextthought.slide'

	image = alias('slideimage')
	number = alias('slidenumber')
	video = alias('slidevideoid')
	slide_deck = deck = alias('slidedeckid')
	end = video_end = alias('slidevideoend')
	start = video_start = alias('slidevideostart')
	
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)


@interface.implementer(INTISlideVideo, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTISlideVideo(SchemaConfigured,
					PersistentPropertyHolder,
					Contained):
	createDirectFieldProperties(INTISlideVideo)

	__external_class_name__ = u"NTISlideVideo"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidevideo'

	Creator = alias('creator')
	video = alias('video_ntiid')
	slide_deck = deck = alias('slidedeckid')
	
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)

@interface.implementer(INTISlideDeck, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTISlideDeck( SchemaConfigured,
					PersistentPropertyHolder,
					Contained):
	createDirectFieldProperties(INTISlideDeck)

	__external_class_name__ = u"NTISlideDeck"
	mime_type = mimeType = u'application/vnd.nextthought.ntislidedeck'

	slides = alias('Slides')
	videos = alias('Videos')
	Creator = alias('creator')
	id = alias('slidedeckid')
	
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
