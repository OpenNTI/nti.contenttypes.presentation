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

from .interfaces import INTIAudio
from .interfaces import INTIMedia
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTITranscript
from .interfaces import INTIAudioSource
from .interfaces import INTIVideoSource

@interface.implementer(INTITranscript, IContentTypeAware)
@WithRepr
class NTITranscript(SchemaConfigured,
					PersistentPropertyHolder,
					Contained):
	createDirectFieldProperties(INTITranscript)

	__external_class_name__ = u"Transcript"
	mime_type = mimeType = u'application/vnd.nextthought.ntitranscript'

	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
	
@interface.implementer(INTIAudioSource, IContentTypeAware)
@WithRepr
class NTIAudioSource(SchemaConfigured,
					 PersistentPropertyHolder,
					 Contained):
	createDirectFieldProperties(INTIAudioSource)

	__external_class_name__ = u"VideoSource"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudiosource'

	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
					
@interface.implementer(INTIVideoSource, IContentTypeAware)
@WithRepr
class NTIVideoSource(SchemaConfigured,
					 PersistentPropertyHolder,
					 Contained):
	createDirectFieldProperties(INTIVideoSource)

	__external_class_name__ = u"VideoSource"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideosource'

	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)

@interface.implementer(INTIMedia, IContentTypeAware)
@WithRepr
@EqHash('ntiid')
class NTIMedia(SchemaConfigured,
			   PersistentPropertyHolder,
			   Contained):
	
	Creator = alias('creator')
	
	def __init__(self, *args, **kwargs):
		SchemaConfigured.__init__(self, *args, **kwargs)
		PersistentPropertyHolder.__init__(self, *args, **kwargs)
		
@interface.implementer(INTIVideo)
@WithRepr
class NTIVideo(NTIMedia):
	createDirectFieldProperties(INTIVideo)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideo'

	closedCaption = closedCaptions = alias('closed_caption')

@interface.implementer(INTIVideoRef, IContentTypeAware)
@WithRepr
class NTIVideoRef(SchemaConfigured,
				  PersistentPropertyHolder,
				  Contained):
	createDirectFieldProperties(INTIVideoRef)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideoref'

@interface.implementer(INTIAudio, IContentTypeAware)
@WithRepr
class NTIAudio(NTIMedia):
	createDirectFieldProperties(INTIAudio)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudio'

@interface.implementer(INTIAudioRef, IContentTypeAware)
@WithRepr
class NTIAudioRef(SchemaConfigured,
				  PersistentPropertyHolder,
				  Contained):
	createDirectFieldProperties(INTIAudioRef)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudioref'
