#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.mimetype.interfaces import IContentTypeAware

from persistent.list import PersistentList

from nti.common.property import alias

from nti.contenttypes.presentation import NTI_AUDIO_REF
from nti.contenttypes.presentation import NTI_VIDEO_REF
from nti.contenttypes.presentation import NTI_AUDIO_ROLL
from nti.contenttypes.presentation import NTI_VIDEO_ROLL

from nti.contenttypes.presentation._base import PersistentMixin
from nti.contenttypes.presentation._base import PersistentPresentationAsset

from nti.contenttypes.presentation.interfaces import EVERYONE
from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIMedia
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIMediaRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIAudioSource
from nti.contenttypes.presentation.interfaces import INTIVideoSource

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

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

@total_ordering
@EqHash('ntiid')
@interface.implementer(INTIMedia)
class NTIMedia(PersistentPresentationAsset):
	createDirectFieldProperties(INTIMedia)

	__external_class_name__ = u"Media"
	mime_type = mimeType = u'application/vnd.nextthought.ntimedia'

	Creator = alias('creator')

	def __lt__(self, other):
		try:
			return (self.mimeType, self.title) < (other.mimeType, other.title)
		except AttributeError:
			return NotImplemented

	def __gt__(self, other):
		try:
			return (self.mimeType, self.title) > (other.mimeType, other.title)
		except AttributeError:
			return NotImplemented

@interface.implementer(INTIMediaRef)
class NTIMediaRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIMediaRef)

	__external_class_name__ = u"MediaRef"
	mime_type = mimeType = u'application/vnd.nextthought.ntimediaref'

	nttype = 'NTIMediaRef'
	visibility = EVERYONE
	Creator = alias('creator')

	__name__ = alias('ntiid')

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

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(self.nttype)
		return self.ntiid

	def __getitem__(self, index):
		item = self.items[index]
		return item

	def __setitem__(self, index, item):
		assert INTIMediaRef.providedBy(item)
		item.__parent__ = self  # take ownership
		self.items[index] = item

	def __len__(self):
		result = len(self.items or ())  # include weak refs
		return result

	def __iter__(self):
		return iter(self.items or ())

	def __contains__(self, obj):
		ntiid = getattr(obj, 'ntiid', None) or str(obj)
		for item in self:
			if item.ntiid == ntiid:
				return True
		return False

	def append(self, item):
		assert INTIMediaRef.providedBy(item)
		item.__parent__ = self  # take ownership
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
			obj.__parent__ = self  # take ownership
			self.items.insert(index, obj)

	def remove(self, item):
		try:
			if self.items:
				self.items.remove(item)
				return True
		except ValueError:
			pass
		return False

	def reset(self, *args, **kwargs):
		result = len(self)
		if self.items:
			del self.items[:]
		return result
	clear = reset

@interface.implementer(INTIAudioRoll)
class NTIAudioRoll(NTIMediaRoll):
	createDirectFieldProperties(INTIAudioRoll)

	nttype = NTI_AUDIO_ROLL
	__external_class_name__ = u"AudioRoll"
	mime_type = mimeType = u'application/vnd.nextthought.ntiaudioroll'

@interface.implementer(INTIVideoRoll)
class NTIVideoRoll(NTIMediaRoll):
	createDirectFieldProperties(INTIVideoRoll)

	nttype = NTI_VIDEO_ROLL
	# For legacy reasons, these are the classes need for IPAD
	# and mimetype needed for the webapp to match up.
	__external_class_name__ = u"ContentVideoCollection"
	mime_type = mimeType = u'application/vnd.nextthought.videoroll'

def media_to_mediaref(media):
	if INTIAudio.providedBy(media):
		result = INTIAudioRef(media)
	else:
		result = INTIVideoRef(media)
	return result
