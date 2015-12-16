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

from persistent.list import PersistentList

from nti.common.property import alias

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentMixin
from ._base import PersistentPresentationAsset

from .interfaces import EVERYONE

from .interfaces import INTIAudio
from .interfaces import INTIMedia
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIMediaRef
from .interfaces import INTIVideoRef
from .interfaces import INTIAudioRoll
from .interfaces import INTIMediaRoll
from .interfaces import INTIVideoRoll
from .interfaces import INTITranscript
from .interfaces import INTIAudioSource
from .interfaces import INTIVideoSource

from . import NTI_AUDIO_REF
from . import NTI_VIDEO_REF

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

@EqHash('ntiid')
@interface.implementer(INTIMedia)
class NTIMedia(PersistentPresentationAsset):
	createDirectFieldProperties(INTIMedia)

	__external_class_name__ = u"Media"
	mime_type = mimeType = u'application/vnd.nextthought.ntimedia'

	Creator = alias('creator')

@interface.implementer(INTIMediaRef)
class NTIMediaRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIMediaRef)

	__external_class_name__ = u"MediaRef"
	mime_type = mimeType = u'application/vnd.nextthought.ntimediaref'

	nttype = 'NTIMediaRef'
	visibility = EVERYONE
	Creator = alias('creator')

	@readproperty
	def target(self):
		return self.ntiid

@interface.implementer(INTIVideo)
class NTIVideo(NTIMedia):
	createDirectFieldProperties(INTIVideo)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideo'

	closedCaption = closedCaptions = alias('closed_caption')

@interface.implementer(INTIVideoRef)
class NTIVideoRef(NTIMediaRef):
	createDirectFieldProperties(INTIVideoRef)

	__external_class_name__ = u"Video"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideoref'

	nttype = NTI_VIDEO_REF

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(self.nttype)
		return self.ntiid

@interface.implementer(INTIAudio)
class NTIAudio(NTIMedia):
	createDirectFieldProperties(INTIAudio)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudio'

@interface.implementer(INTIAudioRef)
class NTIAudioRef(NTIMediaRef):
	createDirectFieldProperties(INTIAudioRef)

	__external_class_name__ = u"Audio"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudioref'

	nttype = NTI_AUDIO_REF

@EqHash('ntiid')
@interface.implementer(INTIMediaRoll)
class NTIMediaRoll(PersistentPresentationAsset):
	createDirectFieldProperties(INTIMediaRoll)

	__external_class_name__ = u"MediaRoll"
	mime_type = mimeType = u'application/vnd.nextthought.ntimediaroll'

	items = alias('Items')
	Creator = alias('creator')

	def __getitem__(self, index):
		item = self.items[index]
		return item

	def __setitem__(self, index, item):
		self.items[index] = item

	def __len__(self):
		result = len(self.items or ())  # include weak refs
		return result

	def __iter__(self):
		return iter(self.items or ())

	def append(self, item):
		assert INTIMediaRef.providedBy(item)
		self.items = PersistentList() if self.items is None else self.items
		self.items.append(item)
	add = append

	def pop(self, index):
		self.items.pop(index)

	def insert(self, index, obj):
		# Remove from our list if it exists, and then insert at.
		self.remove(obj)
		if index is None or index >= len(self):
			# Default to append.
			self.append(obj)
		else:
			self.items.insert(index, obj)

	def remove(self, item):
		try:
			if self.items:
				self.items.remove(item)
				return True
		except ValueError:
			pass
		return False

@interface.implementer(INTIAudioRoll)
class NTIAudioRoll(NTIMediaRoll):
	createDirectFieldProperties(INTIAudioRoll)

	__external_class_name__ = u"AudioRoll"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudioroll'

@interface.implementer(INTIVideoRoll)
class NTIVideoRoll(NTIMediaRoll):
	createDirectFieldProperties(INTIVideoRoll)

	__external_class_name__ = u"VideoRoll"
	mime_type = mimeType = u'application/vnd.nextthought.ntivideoroll'
