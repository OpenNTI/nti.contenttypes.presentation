#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.schema.interfaces import IList
from zope.schema.interfaces import IChoice

from nti.contenttypes.presentation import FIELDS
from nti.contenttypes.presentation import ACCEPTS
from nti.contenttypes.presentation import MEDIA_REF_INTERFACES
from nti.contenttypes.presentation import GROUP_OVERVIEWABLE_INTERFACES

from nti.contenttypes.presentation.common import make_schema
from nti.contenttypes.presentation.common import get_visibility_options

from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTISlide
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTIAudioRoll
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import INTIVideoRoll
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIAudioSource
from nti.contenttypes.presentation.interfaces import INTIVideoSource
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemaMaker

from nti.contenttypes.presentation.schema import VisibilityField

from nti.coremetadata.jsonschema import CoreJsonSchemafier

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.schema.interfaces import IVariant

ITEMS = StandardExternalFields.ITEMS

class BaseJsonSchemafier(CoreJsonSchemafier):

	def post_process_field(self, name, field, item_schema):
		super(BaseJsonSchemafier, self).post_process_field(name, field, item_schema)
		if isinstance(field, VisibilityField):
			item_schema['type'] = 'Choice'
			item_schema['choices'] = sorted(get_visibility_options())

class MediaSourceJsonSchemafier(BaseJsonSchemafier):

	def post_process_field(self, name, field, item_schema):
		super(MediaSourceJsonSchemafier, self).post_process_field(name, field, item_schema)

		# handle type field
		if 		name == 'type' \
			and IList.providedBy(field) \
			and IChoice.providedBy(field.value_type):
			choices, _ = self.get_data_from_choice_field(field.value_type)
			item_schema['choices'] = sorted(choices)

		# handle source field
		if 		name == 'source' \
			and IList.providedBy(field) \
			and IVariant.providedBy(field.value_type):
			for x in field.value_type.fields:
				if IChoice.providedBy(x):
					choices, _ = self.get_data_from_choice_field(x)
					item_schema['choices'] = sorted(choices)

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class PresentationAssetJsonSchemaMaker(object):

	maker = BaseJsonSchemafier

	def make_schema(self, schema=IPresentationAsset, user=None):
		result = LocatedExternalDict()
		maker = self.maker(schema)
		result[FIELDS] = maker.make_schema()
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class ItemContainerJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	has_items = True
	ref_interfaces = ()

	def make_schema(self, schema=IPresentationAsset, user=None):
		result = super(ItemContainerJsonSchemaMaker, self).make_schema(schema, user=user)
		accepts = result[ACCEPTS] = {}
		for iface in self.ref_interfaces:
			mimeType = iface.getTaggedValue('_ext_mime_type')
			accepts[mimeType] = make_schema(schema=iface).get(FIELDS)
		if self.has_items:
			fields = result[FIELDS]
			base_types = sorted(accepts.keys())
			fields[ITEMS]['base_type'] = base_types if len(base_types) > 1 else base_types[0]
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class SlideDeckJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	has_items = False
	ref_interfaces = (INTISlide, INTISlideVideo)

	def make_schema(self, schema=INTISlideDeck, user=None):
		result = super(SlideDeckJsonSchemaMaker, self).make_schema(INTISlideDeck, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	maker = MediaSourceJsonSchemafier

	def make_schema(self, schema=INTIAudioSource, user=None):
		result = super(AudioSourceJsonSchemaMaker, self).make_schema(INTIAudioSource, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	maker = MediaSourceJsonSchemafier

	def make_schema(self, schema=INTIVideoSource, user=None):
		result = super(VideoSourceJsonSchemaMaker, self).make_schema(INTIVideoSource, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	has_items = False
	ref_interfaces = (INTITranscript, INTIVideoSource)

	def make_schema(self, schema=INTIVideo, user=None):
		result = super(VideoJsonSchemaMaker, self).make_schema(INTIVideo, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	has_items = False
	ref_interfaces = (INTITranscript, INTIAudioSource)

	def make_schema(self, schema=INTIAudio, user=None):
		result = super(AudioJsonSchemaMaker, self).make_schema(INTIAudio, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class MediaRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = MEDIA_REF_INTERFACES

	def make_schema(self, schema=INTIMediaRoll, user=None):
		result = super(MediaRollJsonSchemaMaker, self).make_schema(INTIMediaRoll, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTIVideoRef,)

	def make_schema(self, schema=INTIVideoRoll, user=None):
		result = super(VideoRollJsonSchemaMaker, self).make_schema(INTIVideoRoll, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTIAudioRef,)

	def make_schema(self, schema=INTIAudioRoll, user=None):
		result = super(AudioRollJsonSchemaMaker, self).make_schema(INTIAudioRoll, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class CourseOverviewGroupJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = GROUP_OVERVIEWABLE_INTERFACES

	def make_schema(self, schema=INTICourseOverviewGroup, user=None):
		result = super(CourseOverviewGroupJsonSchemaMaker, self).make_schema(INTICourseOverviewGroup, user=user)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class LessonOverviewJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTICourseOverviewGroup,)

	def make_schema(self, schema=INTILessonOverview, user=None):
		result = super(LessonOverviewJsonSchemaMaker, self).make_schema(INTILessonOverview, user=user)
		return result
