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
from zope.schema.interfaces import IObject

from nti.contenttypes.presentation import FIELDS
from nti.contenttypes.presentation import ACCEPTS
from nti.contenttypes.presentation import MEDIA_REF_INTERFACES
from nti.contenttypes.presentation import GROUP_OVERVIEWABLE_INTERFACES

from nti.contenttypes.presentation.common import make_schema

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

from nti.coremetadata.interfaces import ICreated
from nti.coremetadata.interfaces import IRecordable
from nti.coremetadata.interfaces import ICreatedTime
from nti.coremetadata.interfaces import ILastModified
from nti.coremetadata.interfaces import IRecordableContainer

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.schema.interfaces import IVariant

from nti.schema.jsonschema import get_ui_types_from_field
from nti.schema.jsonschema import get_ui_type_from_interface
from nti.schema.jsonschema import get_data_from_choice_field
from nti.schema.jsonschema import get_ui_type_from_field_interface

from nti.schema.jsonschema import JsonSchemafier

ITEMS = StandardExternalFields.ITEMS

class BaseJsonSchemafier(JsonSchemafier):

	def allow_field(self, name, field):
		if	 name.startswith('_') \
			or name in ICreated \
			or name in IRecordable \
			or name in ICreatedTime \
			or name in ILastModified \
			or name in IRecordableContainer \
			or field.queryTaggedValue('_ext_excluded_out'):
			return False
		return True

	def _process_object(self, field):
		if	  IObject.providedBy(field) \
			and field.schema is not interface.Interface:
			base =      field.schema.queryTaggedValue('_ext_mime_type') \
					or  get_ui_type_from_field_interface(field.schema) \
					or  get_ui_type_from_interface(field.schema)
			return base
		return None

	def _process_variant(self, field, ui_type):
		base_types = set()
		for field in field.fields:
			base = get_ui_types_from_field(field)[1]
			if not base:
				if IObject.providedBy(field):
					base = self._process_object(field)
				if IChoice.providedBy(field):
					_, base = get_data_from_choice_field(field)
			if base:
				base_types.add(base.lower())
		if base_types:
			base_types = sorted(base_types, reverse=True)
			ui_base_type = base_types[0] if len(base_types) == 1 else base_types
		else:
			ui_base_type = ui_type
		return ui_base_type

	def get_ui_types_from_field(self, field):
		ui_type, ui_base_type = super(BaseJsonSchemafier, self).get_ui_types_from_field(field)
		if IVariant.providedBy(field) and not ui_base_type:
			ui_base_type = self._process_variant(field, ui_type)
		elif IList.providedBy(field) and not ui_base_type:
			if IObject.providedBy(field.value_type):
				ui_base_type = self._process_object(field.value_type)
			elif IChoice.providedBy(field.value_type):
				_, ui_base_type = get_data_from_choice_field(field.value_type)
			elif IVariant.providedBy(field.value_type):
				ui_base_type = self._process_variant(field.value_type, ui_type)
		return ui_type, ui_base_type

class MediaSourceJsonSchemafier(BaseJsonSchemafier):

	def post_process_field(self, name, field, item_schema):
		super(MediaSourceJsonSchemafier, self).post_process_field(name, field, item_schema)

		# handle type field
		if 		name == 'type' \
			and IList.providedBy(field) \
			and IChoice.providedBy(field.value_type):
			choices, _ = get_data_from_choice_field(field.value_type)
			item_schema['choices'] = sorted(choices)

		# handle source field
		if 		name == 'source' \
			and IList.providedBy(field) \
			and IVariant.providedBy(field.value_type):
			for x in field.value_type.fields:
				if IChoice.providedBy(x):
					choices, _ = get_data_from_choice_field(x)
					item_schema['choices'] = sorted(choices)

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class PresentationAssetJsonSchemaMaker(object):

	maker = BaseJsonSchemafier

	def make_schema(self, schema=IPresentationAsset):
		result = LocatedExternalDict()
		maker = self.maker(schema)
		result[FIELDS] = maker.make_schema()
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class ItemContainerJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	has_items = True
	ref_interfaces = ()

	def make_schema(self, schema=IPresentationAsset):
		result = super(ItemContainerJsonSchemaMaker, self).make_schema(schema)
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

	def make_schema(self, schema=INTISlideDeck):
		result = super(SlideDeckJsonSchemaMaker, self).make_schema(INTISlideDeck)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	maker = MediaSourceJsonSchemafier

	def make_schema(self, schema=INTIAudioSource):
		result = super(AudioSourceJsonSchemaMaker, self).make_schema(INTIAudioSource)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoSourceJsonSchemaMaker(PresentationAssetJsonSchemaMaker):

	maker = MediaSourceJsonSchemafier

	def make_schema(self, schema=INTIVideoSource):
		result = super(VideoSourceJsonSchemaMaker, self).make_schema(INTIVideoSource)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	has_items = False
	ref_interfaces = (INTITranscript, INTIVideoSource)

	def make_schema(self, schema=INTIVideo):
		result = super(VideoJsonSchemaMaker, self).make_schema(INTIVideo)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class MediaRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = MEDIA_REF_INTERFACES

	def make_schema(self, schema=INTIMediaRoll):
		result = super(MediaRollJsonSchemaMaker, self).make_schema(INTIMediaRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class VideoRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTIVideoRef,)

	def make_schema(self, schema=INTIVideoRoll):
		result = super(VideoRollJsonSchemaMaker, self).make_schema(INTIVideoRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class AudioRollJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTIAudioRef,)

	def make_schema(self, schema=INTIAudioRoll):
		result = super(AudioRollJsonSchemaMaker, self).make_schema(INTIAudioRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class CourseOverviewGroupJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = GROUP_OVERVIEWABLE_INTERFACES

	def make_schema(self, schema=INTICourseOverviewGroup):
		result = super(CourseOverviewGroupJsonSchemaMaker, self).make_schema(INTICourseOverviewGroup)
		return result

@interface.implementer(IPresentationAssetJsonSchemaMaker)
class LessonOverviewJsonSchemaMaker(ItemContainerJsonSchemaMaker):

	ref_interfaces = (INTICourseOverviewGroup,)

	def make_schema(self, schema=INTILessonOverview):
		result = super(LessonOverviewJsonSchemaMaker, self).make_schema(INTILessonOverview)
		return result
