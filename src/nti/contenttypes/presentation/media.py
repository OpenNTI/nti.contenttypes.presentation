#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.mimetype.interfaces import IContentTypeAware

from nti.common.property import alias

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentMixin
from ._base import PersistentPresentationAsset

from .interfaces import INTIAudio
from .interfaces import INTIMedia
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTITranscript
from .interfaces import INTIAudioSource
from .interfaces import INTIVideoSource

@interface.implementer(INTITranscript, IContentTypeAware)
class NTITranscript(PersistentMixin):
	createDirectFieldProperties(INTITranscript)

	__external_class_name__ = u"Transcript"
	mime_type = mimeType = u'application/vnd.nextthought.ntitranscript'
	
@interface.implementer(INTIAudioSource, IContentTypeAware)
class NTIAudioSource(PersistentMixin):
	createDirectFieldProperties(INTIAudioSource)

	__external_class_name__ = u"VideoSource"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudiosource'
					
@interface.implementer(INTIVideoSource, IContentTypeAware)
class NTIVideoSource(PersistentMixin):
	createDirectFieldProperties(INTIVideoSource)

	__external_class_name__ = u"VideoSource"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideosource'

@interface.implementer(INTIMedia)
@EqHash('ntiid')
class NTIMedia(PersistentPresentationAsset):
	
	Creator = alias('creator')
		
@interface.implementer(INTIVideo)
class NTIVideo(NTIMedia):
	createDirectFieldProperties(INTIVideo)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideo'

	closedCaption = closedCaptions = alias('closed_caption')

@interface.implementer(INTIVideoRef)
class NTIVideoRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIVideoRef)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideoref'
	
	visibility = u"everyone"
	
	@readproperty
	def target(self):
		return self.ntiid

@interface.implementer(INTIAudio)
class NTIAudio(NTIMedia):
	createDirectFieldProperties(INTIAudio)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudio'

@interface.implementer(INTIAudioRef)
class NTIAudioRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIAudioRef)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudioref'
	
	visibility = u"everyone"
	
	@readproperty
	def target(self):
		return self.ntiid
