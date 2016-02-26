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
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemafier

from nti.coremetadata.interfaces import ICreated
from nti.coremetadata.interfaces import IRecordable
from nti.coremetadata.interfaces import ICreatedTime
from nti.coremetadata.interfaces import ILastModified
from nti.coremetadata.interfaces import IRecordableContainer

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.schema.interfaces import IVariant

from nti.schema.jsonschema import ui_type_from_field
from nti.schema.jsonschema import process_choice_field
from nti.schema.jsonschema import interface_to_ui_type
from nti.schema.jsonschema import ui_type_from_field_iface

from nti.schema.jsonschema import JsonSchemafier as JsonSchemaMaker

ITEMS = StandardExternalFields.ITEMS

class BaseJsonSchemaMaker(JsonSchemaMaker):

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
					or  ui_type_from_field_iface(field.schema) \
					or  interface_to_ui_type(field.schema)
			return base
		return None

	def _process_variant(self, field, ui_type):
		base_types = set()
		for field in field.fields:
			base = ui_type_from_field(field)[1]
			if not base:
				if IObject.providedBy(field):
					base = self._process_object(field)
				if IChoice.providedBy(field):
					_, base = process_choice_field(field)
			if base:
				base_types.add(base.lower())
		if base_types:
			base_types = sorted(base_types, reverse=True)
			ui_base_type = base_types[0] if len(base_types) == 1 else base_types
		else:
			ui_base_type = ui_type
		return ui_base_type

	def ui_types_from_field(self, field):
		ui_type, ui_base_type = super(BaseJsonSchemaMaker, self).ui_types_from_field(field)
		if IVariant.providedBy(field) and not ui_base_type:
			ui_base_type = self._process_variant(field, ui_type)
		elif IList.providedBy(field) and not ui_base_type:
			if IObject.providedBy(field.value_type):
				ui_base_type = self._process_object(field.value_type)
			elif IChoice.providedBy(field.value_type):
				_, ui_base_type = process_choice_field(field.value_type)
			elif IVariant.providedBy(field.value_type):
				ui_base_type = self._process_variant(field.value_type, ui_type)
		return ui_type, ui_base_type

class MediaSourceJsonSchemaMaker(BaseJsonSchemaMaker):

	def post_process_field(self, name, field, item_schema):
		super(MediaSourceJsonSchemaMaker, self).post_process_field(name, field, item_schema)
		if name == 'type':
			choices, _ = process_choice_field(field.value_type)
			item_schema['choices'] = sorted(choices)

@interface.implementer(IPresentationAssetJsonSchemafier)
class PresentationAssetJsonSchemafier(object):

	maker = BaseJsonSchemaMaker

	def make_schema(self, schema=IPresentationAsset):
		result = LocatedExternalDict()
		maker = self.maker(schema)
		result[FIELDS] = maker.make_schema()
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class ItemContainerJsonSchemafier(PresentationAssetJsonSchemafier):

	has_items = True
	ref_interfaces = ()

	def make_schema(self, schema=IPresentationAsset):
		result = super(ItemContainerJsonSchemafier, self).make_schema(schema)
		accepts = result[ACCEPTS] = {}
		for iface in self.ref_interfaces:
			mimeType = iface.getTaggedValue('_ext_mime_type')
			accepts[mimeType] = make_schema(schema=iface).get(FIELDS)
		if self.has_items:
			fields = result[FIELDS]
			base_types = sorted(accepts.keys())
			fields[ITEMS]['base_type'] = base_types if len(base_types) > 1 else base_types[0]
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class SlideDeckJsonSchemafier(ItemContainerJsonSchemafier):

	has_items = False
	ref_interfaces = (INTISlide, INTISlideVideo)

	def make_schema(self, schema=INTISlideDeck):
		result = super(SlideDeckJsonSchemafier, self).make_schema(INTISlideDeck)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class AudioSourceJsonSchemafier(PresentationAssetJsonSchemafier):

	maker = MediaSourceJsonSchemaMaker

	def make_schema(self, schema=INTIAudioSource):
		result = super(AudioSourceJsonSchemafier, self).make_schema(INTIAudioSource)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class VideoSourceJsonSchemafier(PresentationAssetJsonSchemafier):

	maker = MediaSourceJsonSchemaMaker

	def make_schema(self, schema=INTIVideoSource):
		result = super(VideoSourceJsonSchemafier, self).make_schema(INTIVideoSource)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class VideoJsonSchemafier(ItemContainerJsonSchemafier):

	has_items = False
	ref_interfaces = (INTITranscript, INTIVideoSource)

	def make_schema(self, schema=INTIVideo):
		result = super(VideoJsonSchemafier, self).make_schema(INTIVideo)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class MediaRollJsonSchemafier(ItemContainerJsonSchemafier):

	ref_interfaces = MEDIA_REF_INTERFACES

	def make_schema(self, schema=INTIMediaRoll):
		result = super(MediaRollJsonSchemafier, self).make_schema(INTIMediaRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class VideoRollJsonSchemafier(ItemContainerJsonSchemafier):

	ref_interfaces = (INTIVideoRef,)

	def make_schema(self, schema=INTIVideoRoll):
		result = super(VideoRollJsonSchemafier, self).make_schema(INTIVideoRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class AudioRollJsonSchemafier(ItemContainerJsonSchemafier):

	ref_interfaces = (INTIAudioRef,)

	def make_schema(self, schema=INTIAudioRoll):
		result = super(AudioRollJsonSchemafier, self).make_schema(INTIAudioRoll)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class CourseOverviewGroupJsonSchemafier(ItemContainerJsonSchemafier):

	ref_interfaces = GROUP_OVERVIEWABLE_INTERFACES

	def make_schema(self, schema=INTICourseOverviewGroup):
		result = super(CourseOverviewGroupJsonSchemafier, self).make_schema(INTICourseOverviewGroup)
		return result

@interface.implementer(IPresentationAssetJsonSchemafier)
class LessonOverviewJsonSchemafier(ItemContainerJsonSchemafier):

	ref_interfaces = (INTICourseOverviewGroup,)

	def make_schema(self, schema=INTILessonOverview):
		result = super(LessonOverviewJsonSchemafier, self).make_schema(INTILessonOverview)
		return result
