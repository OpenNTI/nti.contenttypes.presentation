#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from copy import copy

from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable

from zope.dublincore.interfaces import IDCDescriptiveProperties

from zope.interface.common.mapping import IMapping
from zope.interface.common.sequence import IFiniteSequence

from zope.interface.interfaces import ObjectEvent
from zope.interface.interfaces import IObjectEvent

from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zope.location.interfaces import IContained

from zope.schema import vocabulary

from dolmen.builtins.interfaces import IIterable

from nti.common.property import alias

from nti.coremetadata.interfaces import ITitled
from nti.coremetadata.interfaces import ICreated
from nti.coremetadata.interfaces import IRecordable
from nti.coremetadata.interfaces import ILastModified
from nti.coremetadata.interfaces import IRecordableContainer

from nti.namedfile.interfaces import INamedFile

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Int
from nti.schema.field import Bool
from nti.schema.field import Choice
from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import Variant
from nti.schema.field import Iterable
from nti.schema.field import ValidURI
from nti.schema.field import ValidText
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable
from nti.schema.jsonschema import TAG_HIDDEN_IN_UI
from nti.schema.jsonschema import TAG_REQUIRED_IN_UI

# Transcript types (file extensions)

SBV_TRANSCRIPT_TYPE = u'sbv'
SRT_TRANSCRIPT_TYPE = u'srt'
VTT_TRANSCRIPT_TYPE = u'vtt'
TRANSCRIPT_TYPES = (SBV_TRANSCRIPT_TYPE, SRT_TRANSCRIPT_TYPE, VTT_TRANSCRIPT_TYPE)

TRANSCRIPT_TYPE_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in TRANSCRIPT_TYPES])

# Transcript MimeTypes

SBV_TRANSCRIPT_MIMETYPE = u'text/sbv'
SRT_TRANSCRIPT_MIMETYPE = u'text/srt'
VTT_TRANSCRIPT_MIMETYPE = u'text/vtt'
TRANSCRIPT_MIMETYPES = (SBV_TRANSCRIPT_MIMETYPE, SRT_TRANSCRIPT_MIMETYPE,
						VTT_TRANSCRIPT_MIMETYPE)

TRANSCRIPT_MIMETYPE_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in TRANSCRIPT_MIMETYPES])

# Video Services

HTML5_VIDEO_SERVICE = u'html5'
VIMEO_VIDEO_SERVICE = u'vimeo'
YOUTUBE_VIDEO_SERVICE = u'youtube'
KALTURA_VIDEO_SERVICE = u'kaltura'
VIDEO_SERVICES = (HTML5_VIDEO_SERVICE, VIMEO_VIDEO_SERVICE, YOUTUBE_VIDEO_SERVICE,
				  KALTURA_VIDEO_SERVICE)

VIDEO_SERVICES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VIDEO_SERVICES])

# Video Service Types

MP4_VIDEO_SERVICE_TYPE = u'video/mp4'
WEBM_VIDEO_SERVICE_TYPE = u'video/webm'
VIMEO_VIDEO_SERVICE_TYPE = u'video/vimeo'
YOUTUBE_VIDEO_SERVICE_TYPE = u'video/youtube'
KALTURA_VIDEO_SERVICE_TYPE = u'video/kaltura'

VIDEO_SERVICE_TYPES = (MP4_VIDEO_SERVICE_TYPE, WEBM_VIDEO_SERVICE_TYPE,
					   YOUTUBE_VIDEO_SERVICE_TYPE, VIMEO_VIDEO_SERVICE_TYPE,
					   KALTURA_VIDEO_SERVICE_TYPE)

VIDEO_SERVICE_TYPES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VIDEO_SERVICE_TYPES])

# Video Service Sources

MP4_VIDEO_SOURCE = u'mp4'
WEBM_VIDEO_SOURCE = u'webm'
OTHER_VIDEO_SOURCE = u'other'
VIDEO_SOURCES = (MP4_VIDEO_SOURCE, WEBM_VIDEO_SOURCE, OTHER_VIDEO_SOURCE)

VIDEO_SOURCES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VIDEO_SOURCES])

# Audio Services

HTML5_AUDIO_SERVICE = u'html5'
AUDIO_SERVICES = (HTML5_AUDIO_SERVICE,)

AUDIO_SERVICES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in AUDIO_SERVICES])

# Audio Service Types

MP3_AUDIO_SERVICE_TYPE = u'audio/mp3'
WAV_AUDIO_SERVICE_TYPE = u'audio/wav'

AUDIO_SERVICE_TYPES = (MP3_AUDIO_SERVICE_TYPE, WAV_AUDIO_SERVICE_TYPE)

AUDIO_SERVICE_TYPES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in AUDIO_SERVICE_TYPES])

# Audio Service Sources

MP3_AUDIO_SOURCE = u'mp4'
WAV_AUDIO_SOURCE = u'webm'
OTHER_AUDIO_SOURCE = u'other'
AUDIO_SOURCES = (MP3_AUDIO_SOURCE, WAV_AUDIO_SOURCE, OTHER_AUDIO_SOURCE)

AUDIO_SOURCES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in AUDIO_SOURCES])

OU = "OU"
PUBLIC = u'Public'
CREDIT = "ForCredit"
EVERYONE = u'everyone'
PURCHASED = "Purchased"
VISIBILITY = (PUBLIC, CREDIT, EVERYONE, PURCHASED, OU)

VISIBILITY_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VISIBILITY])

def byline_schema_field(required=False):
	return Variant((ValidTextLine(title="Creator name"),
					Object(interface.Interface, title="Creator object")),
					required=required)

def href_schema_field(title=u'', required=False, default=None):
	return Variant((ValidTextLine(title="href name"),
					ValidURI(title="href source uri"),
					Object(INamedFile, title="href file")),
					title=title,
					default=default,
					required=required)

class ITaggedContent(interface.Interface):
	"""
	Something that can contain tags.
	"""

	tags = IndexedIterable(title="Tags applied by the user.",
					  	   value_type=ValidTextLine(min_length=1, title="A single tag"),
					   	   unique=True,
					   	   default=(),
					  	   required=False)

class IPresentationAsset(ILastModified, IContained, IRecordable, IAttributeAnnotatable):
	"""
	marker interface for all presentation assests
	"""
IPresentationAsset.setTaggedValue('_ext_jsonschema', u'')

class IAssetRef(ICreated):
	target = interface.Attribute("target object id")

class IItemAssetContainer(interface.Interface):

	def append(item):
		"""
		Add an item
		"""

	def remove(item):
		"""
		remove the specified item

		:return True if object was removed
		"""
		
	def __contains__(item):
		"""
		return is the specified item is in this container
		"""

class IGroupOverViewable(interface.Interface):
	"""
	marker interface for things that can be part of a course overview group
	"""
IGroupOverViewable.setTaggedValue('_ext_is_marker_interface', True)

class INTITranscript(ILastModified):
	src = href_schema_field(title="Transcript source", required=True)
	srcjsonp = href_schema_field(title="Transcript source jsonp", required=False)
	lang = ValidTextLine(title="Transcript language", required=True, default='en')
	type = Choice(vocabulary=TRANSCRIPT_MIMETYPE_VOCABULARY, title='Transcript mimetype',
				  required=True, default=VTT_TRANSCRIPT_MIMETYPE)
	purpose = ValidTextLine(title="Transcript purpose", required=True, default='normal')

class INTIIDIdentifiable(interface.Interface):
	ntiid = ValidNTIID(title="Item NTIID", required=False, default=None)

class INTIMediaSource(ILastModified):
	service = ValidTextLine(title="Source service", required=True)
	thumbnail = href_schema_field(title="Source thumbnail", required=False)

class IVisible(interface.Interface):
	"""
	marker interface for things that have visibility
	"""
	visibility = Choice(vocabulary=VISIBILITY_VOCABULARY, title='Media ref visibility',
					 	required=False, default=EVERYONE)

class INTIMediaRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable,
				   IPresentationAsset, IVisible):
	target = ValidNTIID(title="Target NTIID", required=False)
IMediaRef = INTIMediaRef  # BWC

class IAssetTitled( interface.Interface ):
	title = ValidTextLine(title="Asset title", required=False)

class IAssetTitleDescribed( IAssetTitled, IDCDescriptiveProperties ):
	# IDCDescriptiveProperties marker needed for ext adapter.
	title = copy(IAssetTitled['title'])
	title.default = u''
	description = ValidTextLine(title="Media description", required=False, default=u'')

class INTIMedia(IAssetTitleDescribed, INTIIDIdentifiable,
				ICreated, IPresentationAsset):

	byline = byline_schema_field(required=False)

class INTIVideoSource(INTIMediaSource):
	width = Int(title="Video width", required=False)
	height = Int(title="Video height", required=False)
	poster = ValidTextLine(title="Video poster", required=False)
	service = Choice(vocabulary=VIDEO_SERVICES_VOCABULARY, title='Video service',
					 required=True, default=HTML5_VIDEO_SERVICE)

	source = IndexedIterable(Variant((Choice(vocabulary=VIDEO_SOURCES_VOCABULARY),
								  	  ValidTextLine())),
						 	 title='Video source', required=True, min_length=1)

	type = IndexedIterable(Choice(vocabulary=VIDEO_SERVICE_TYPES_VOCABULARY),
					  	   title='Video service types', required=True, min_length=1)

INTIVideoSource.setTaggedValue('_ext_jsonschema', u'videosource')

class INTIVideo(INTIMedia):
	subtitle = Bool(title="Subtitle flag", required=False, default=None)

	closed_caption = Bool(title="Close caption flag", required=False, default=None)

	sources = IndexedIterable(value_type=Object(INTIVideoSource),
						 	  title="The video sources", required=False, min_length=0)

	transcripts = IndexedIterable(value_type=Object(INTITranscript),
							  	  title="The transcripts", required=False, min_length=0)

INTIVideo.setTaggedValue('_ext_jsonschema', u'video')

INTIVideo['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideo['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIVideo['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideo['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIVideoRef(INTIMediaRef):
	label = ValidText(title="Video label", required=False)
	poster = ValidTextLine(title="Video poster", required=False)

INTIVideoRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIVideoRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIAudioSource(INTIMediaSource):
	service = Choice(vocabulary=AUDIO_SERVICES_VOCABULARY, title='Audio service',
					 required=True, default=HTML5_AUDIO_SERVICE)

	source = IndexedIterable(Variant((Choice(vocabulary=AUDIO_SOURCES_VOCABULARY),
								 	  ValidTextLine())),
						 	 title='Audio source', required=True, min_length=1)

	type = IndexedIterable(Choice(vocabulary=AUDIO_SERVICE_TYPES_VOCABULARY),
					   	   title='Audio service types', required=True, min_length=1)

INTIAudioSource.setTaggedValue('_ext_jsonschema', u'audiosource')

class INTIAudio(INTIMedia):
	sources = IndexedIterable(value_type=Object(INTIAudioSource),
						  	  title="The audio sources",
						  	  required=False, min_length=1)

	transcripts = IndexedIterable(value_type=Object(INTITranscript),
							  	  title="The transcripts",
							  	  required=False, min_length=0)

INTIAudio.setTaggedValue('_ext_jsonschema', u'audio')

INTIAudio['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAudio['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIAudio['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAudio['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIAudioRef(INTIMediaRef):
	pass

class INTIMediaRoll(IItemAssetContainer, IGroupOverViewable, INTIIDIdentifiable,
					ICreated, IPresentationAsset, IIterable, IVisible,
					IFiniteSequence):

	Items = IndexedIterable(value_type=Object(INTIMediaRef),
							title="The media sources", required=False, min_length=0)

	def pop(idx):
		"""
		remove the item at the specified index
		"""
INTIMediaRoll.setTaggedValue('_ext_jsonschema', u'mediaroll')

class INTIAudioRoll(INTIMediaRoll):
	Items = IndexedIterable(value_type=Object(INTIAudioRef),
							title="The audio sources", required=False, min_length=0)
INTIAudioRoll.setTaggedValue('_ext_jsonschema', u'audioroll')

class INTIVideoRoll(INTIMediaRoll):
	Items = IndexedIterable(value_type=Object(INTIVideoRef),
							title="The audio sources", required=False, min_length=0)
INTIVideoRoll.setTaggedValue('_ext_jsonschema', u'videoroll')

class INTISlide(INTIIDIdentifiable, IPresentationAsset):
	slidevideoid = ValidNTIID(title="Slide video NTIID", required=True)
	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	slidevideostart = Number(title="Video start", required=False, default=0)
	slidevideoend = Number(title="Video end", required=False, default=0)
	slideimage = href_schema_field(title="Slide image source", required=False)
	slidenumber = Int(title="Slide number", required=True, default=1)

class INTISlideVideo(IAssetTitleDescribed, INTIIDIdentifiable, ICreated, IPresentationAsset):
	byline = byline_schema_field(required=False)
	video_ntiid = ValidNTIID(title="Slide video NTIID", required=True)
	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	thumbnail = href_schema_field(title="Slide video thumbnail", required=False)

INTISlideVideo['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideVideo['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTISlideVideo['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideVideo['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTISlideDeck(IItemAssetContainer, IAssetTitleDescribed, INTIIDIdentifiable,
					ICreated, IPresentationAsset):

	Slides = IndexedIterable(value_type=Object(INTISlide),
						 	 title="The slides", required=False, min_length=1)

	Videos = IndexedIterable(value_type=Object(INTISlideVideo),
						 	 title="The slide videos", required=False, min_length=1)

	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)

	byline = byline_schema_field(required=False)
	
	Items = Iterable(title='All items in the slide deck', readonly=True, required=False)
	Items.setTaggedValue('_ext_excluded_out', True)

INTISlideDeck.setTaggedValue('_ext_jsonschema', u'slidedeck')

INTISlideDeck['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideDeck['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTISlideDeck['description'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISlideDeck['description'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTITimeline(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	label = ValidTextLine(title="The label", required=True, default=u'')
	href = href_schema_field(title="Resource href", required=False, default=u'')
	icon = href_schema_field(title="Icon href", required=False)
	description = ValidTextLine(title="Timeline description", required=False)
	suggested_inline = Bool("Suggested inline flag", required=False, default=False)

INTITimeline['href'].setTaggedValue(TAG_REQUIRED_IN_UI, True)

class INTIRelatedWorkRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable, ICreated,
						 IPresentationAsset, IVisible):
	href = href_schema_field(title="Related work href", required=False, default=u'')
	target = ValidNTIID(title="Target NTIID", required=False)
	byline = byline_schema_field(required=False)
	section = ValidTextLine(title="Section", required=False)
	description = ValidText(title="Slide video description", required=False)
	icon = href_schema_field(title="Related work icon href", required=False)
	type = ValidTextLine(title="The target mimetype", required=False)
	label = ValidTextLine(title="The label", required=False, default=u'')
	ntiid = Variant((ValidTextLine(title="Related content ntiid"),
					 ValidNTIID(title="Related content ntiid")), required=False, default=None)

class INTIDiscussionRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable, ITitled, IPresentationAsset):
	title = ValidTextLine(title="Discussion title", required=False)
	icon = href_schema_field(title="Discussion icon href", required=False)
	label = ValidTextLine(title="The label", required=False, default=u'')
	ntiid = Variant((ValidTextLine(title="Discussion NTIID"),
					 ValidNTIID(title="Discussion NTIID")), required=False, default=None)
	target = Variant((ValidTextLine(title="Target NTIID"),
					  ValidNTIID(title="Target NTIID")), required=False)

	id = ValidTextLine(title="Discussion identifier", required=True)
	id.setTaggedValue('__external_accept_id__', True)

	def isCourseBundle():
		"""
		return if this DiscussionRef refers to a course bundle
		"""

INTIDiscussionRef['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIDiscussionRef['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIDiscussionRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIDiscussionRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIAssessmentRef(IAssetRef, IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	target = ValidNTIID(title="Target NTIID", required=True)
	label = ValidTextLine(title="The label", required=False, default=u'')
IAssessmentRef = INTIAssessmentRef

INTIAssessmentRef['target'].setTaggedValue(TAG_REQUIRED_IN_UI, True)

class INTIQuestionSetRef(INTIAssessmentRef):
	question_count = Int(title="Question count", required=False)
IQuestionSetRef = INTIQuestionSetRef

INTIQuestionSetRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIQuestionSetRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIQuestionRef(INTIAssessmentRef):
	pass
IQuestionRef = INTIQuestionRef

INTIQuestionRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIQuestionRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIAssignmentRef(INTIAssessmentRef, IAssetTitled):
	containerId = ValidNTIID(title="Container NTIID", required=False)
IAssignmentRef = INTIAssignment = INTIAssignmentRef

INTIAssignmentRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAssignmentRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTIAssignmentRef['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIAssignmentRef['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTIInquiryRef(INTIAssessmentRef):
	pass

class INTIPollRef(INTIInquiryRef):
	pass
IPollRef = INTIPollRef

INTIPollRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTIPollRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTISurveyRef(INTIInquiryRef):
	containerId = ValidNTIID(title="Container NTIID", required=False)
	question_count = Int(title="Question count", required=False)
ISurveyRef = INTISurveyRef

INTISurveyRef['label'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTISurveyRef['label'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTICourseOverviewSpacer(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	pass

class INTICourseOverviewGroup(IItemAssetContainer, IAssetTitled, INTIIDIdentifiable,
							  IPresentationAsset, IFiniteSequence, IIterable,
							  IRecordableContainer):

	Items = IndexedIterable(value_type=Object(IGroupOverViewable),
						 	title="The overview items", required=False, min_length=0)
	accentColor = ValidTextLine(title="Overview color", required=False)

INTICourseOverviewGroup.setTaggedValue('_ext_jsonschema', u'overviewgroup')

INTICourseOverviewGroup['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTICourseOverviewGroup['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)
INTICourseOverviewGroup['accentColor'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTICourseOverviewGroup['accentColor'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class INTILessonOverview(IItemAssetContainer, IAssetTitled, INTIIDIdentifiable,
						 IPresentationAsset, IFiniteSequence, IIterable,
						 IRecordableContainer):

	Items = IndexedIterable(value_type=Object(INTICourseOverviewGroup),
						 	title="The overview items", required=False, min_length=0)
	lesson = ValidTextLine(title="Lesson NTIID", required=False)

	def pop(idx):
		"""
		remove the group at the specified index
		"""
INTILessonOverview.setTaggedValue('_ext_jsonschema', u'lesson')

INTILessonOverview['title'].setTaggedValue(TAG_HIDDEN_IN_UI, False)
INTILessonOverview['title'].setTaggedValue(TAG_REQUIRED_IN_UI, False)

class IPresentationVisibility(interface.Interface):
	"""
	marker interface to return the visibility for an object.

	Register as an adapter
	"""

	def visibility():
		pass

class IPresentationAssetContainer(IMapping):
	"""
	Something that is an unordered bag of presentation asset items

	This package provides no implementation of this interface. (But
	something like the content library package may be adaptable to this,
	typically with annotations).
	"""

	def pop(k, *args):
		"""
		remove specified key and return the corresponding value
		*args may contain a single default value, or may not be supplied.
		If key is not found, default is returned if given, otherwise
		KeyError is raised
		"""

class IPresentationAssetAffiliations(interface.Interface):
	"""
	subscriber for a presentation asset containers
	"""

	def containers(item):
		"""
		return the containers that refer to specified item
		"""

class IPresentationAssetJsonSchemaMaker(interface.Interface):
	"""
	Marker interface for a presentation asset Json Schema maker utility
	"""

	def make_schema(schema=IPresentationAsset):
		"""
		Create the JSON schema.
		
		schema: The zope schema to use.
		"""

class IPresentationAssetCreatedEvent(IObjectCreatedEvent):
	principal = interface.Attribute("Creator principal")
	externalValue = interface.Attribute("External object")

@interface.implementer(IPresentationAssetCreatedEvent)
class PresentationAssetCreatedEvent(ObjectCreatedEvent):

	def __init__(self, obj, principal=None, externalValue=None):
		self.object = obj
		self.principal = principal
		self.externalValue = externalValue

class IWillRemovePresentationAssetEvent(IObjectEvent):
	pass

@interface.implementer(IWillRemovePresentationAssetEvent)
class WillRemovePresentationAssetEvent(ObjectEvent):
	pass

#: Asset removed from item asset container
TRX_ASSET_REMOVED_FROM_ITEM_ASSET_CONTAINER = u'assetremovedfromitemcontainer'

class IItemRemovedFromItemAssetContainerEvent(IObjectModifiedEvent):
	pass

@interface.implementer(IItemRemovedFromItemAssetContainerEvent)
class ItemRemovedFromItemAssetContainerEvent(ObjectModifiedEvent):
	pass

#: Overview group moved recorder transaction type.
TRX_OVERVIEW_GROUP_MOVE_TYPE = u'overviewgroupmoved'

class IOverviewGroupMovedEvent(IObjectEvent):
	pass

@interface.implementer(IOverviewGroupMovedEvent)
class OverviewGroupMovedEvent(ObjectEvent):

	group = alias('object')

	def __init__(self, obj, principal=None, index=None):
		super(OverviewGroupMovedEvent, self).__init__(obj)
		self.index = index
		self.principal = principal

#: Asset moved recorder transaction type.
TRX_ASSET_MOVE_TYPE = u'presentationassetmoved'

class IPresentationAssetMovedEvent(IObjectEvent):
	pass

@interface.implementer(IPresentationAssetMovedEvent)
class PresentationAssetMovedEvent(ObjectEvent):

	asset = alias('object')

	def __init__(self, obj, principal=None, index=None):
		super(PresentationAssetMovedEvent, self).__init__(obj)
		self.index = index
		self.principal = principal

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
	"Import from INTIRelatedWorkRef instead",
	INTIRelatedWork='nnti.contenttypes.presentation.interfaces:INTIRelatedWorkRef')
