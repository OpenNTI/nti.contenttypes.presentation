#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface
from zope.interface.common.sequence import IFiniteSequence

from zope.dublincore.interfaces import IDCDescriptiveProperties

from zope.schema import vocabulary

from dolmen.builtins.interfaces import IIterable

from nti.coremetadata.interfaces import ITitled
from nti.coremetadata.interfaces import ICreated
from nti.coremetadata.interfaces import ILastModified

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Int
from nti.schema.field import Bool
from nti.schema.field import Choice
from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import Variant
from nti.schema.field import ValidURI
from nti.schema.field import ValidText
from nti.schema.field import ListOrTuple
from nti.schema.field import ValidTextLine
from nti.schema.field import IndexedIterable

from nti.wref.interfaces import IWeakRef

## Transcript types (file extensions)

SBV_TRANSCRIPT_TYPE = u'sbv'
SRT_TRANSCRIPT_TYPE = u'srt'
VTT_TRANSCRIPT_TYPE = u'vtt'
TRANSCRIPT_TYPES = (SBV_TRANSCRIPT_TYPE, SRT_TRANSCRIPT_TYPE, VTT_TRANSCRIPT_TYPE)

TRANSCRIPT_TYPE_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in TRANSCRIPT_TYPES])
	
## Transcript MimeTypes

SBV_TRANSCRIPT_MIMETYPE = u'text/sbv'
SRT_TRANSCRIPT_MIMETYPE = u'text/srt'
VTT_TRANSCRIPT_MIMETYPE = u'text/vtt'
TRANSCRIPT_MIMETYPES = (SBV_TRANSCRIPT_MIMETYPE, SRT_TRANSCRIPT_MIMETYPE,
						VTT_TRANSCRIPT_MIMETYPE)

TRANSCRIPT_MIMETYPE_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in TRANSCRIPT_MIMETYPES])
	
## Video Services

HTML5_VIDEO_SERVICE = u'html5'
VIMEO_VIDEO_SERVICE = u'vimeo'
YOUTUBE_VIDEO_SERVICE = u'youtube'
KALTURA_VIDEO_SERVICE = u'kaltura'
VIDEO_SERVICES = (HTML5_VIDEO_SERVICE, VIMEO_VIDEO_SERVICE, YOUTUBE_VIDEO_SERVICE,
				  KALTURA_VIDEO_SERVICE)

VIDEO_SERVICES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VIDEO_SERVICES])
	
## Video Service Types

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
	
## Video Service Sources

MP4_VIDEO_SOURCE = u'mp4'
WEBM_VIDEO_SOURCE = u'webm'
OTHER_VIDEO_SOURCE = u'other'
VIDEO_SOURCES = (MP4_VIDEO_SOURCE, WEBM_VIDEO_SOURCE, OTHER_VIDEO_SOURCE)

VIDEO_SOURCES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in VIDEO_SOURCES])

## Audio Services

HTML5_AUDIO_SERVICE = u'html5'
AUDIO_SERVICES = (HTML5_AUDIO_SERVICE,)

AUDIO_SERVICES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in AUDIO_SERVICES])
	
## Audio Service Types

MP3_AUDIO_SERVICE_TYPE = u'audio/mp3'
WAV_AUDIO_SERVICE_TYPE = u'audio/wav'

AUDIO_SERVICE_TYPES = (MP3_AUDIO_SERVICE_TYPE, WAV_AUDIO_SERVICE_TYPE)

AUDIO_SERVICE_TYPES_VOCABULARY = \
	vocabulary.SimpleVocabulary([vocabulary.SimpleTerm(x) for x in AUDIO_SERVICE_TYPES])
	
## Audio Service Sources

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
	
class ITaggedContent(interface.Interface):
	"""
	Something that can contain tags.
	"""

	tags = ListOrTuple(title="Tags applied by the user.",
					   value_type=ValidTextLine(min_length=1, title="A single tag"),
					   unique=True,
					   default=(),
					   required=False)
	
class IPresentationAsset(ILastModified):
	"""
	marker interface for all presentation assests
	"""

class IGroupOverViewable(interface.Interface):
	"""
	marker interface for things that can be part of a course overview group
	"""

class IGroupOverViewableWeakRef(IWeakRef):
	pass

class INTITranscript(IPresentationAsset):
	src = Variant((	ValidTextLine(title="Transcript source"),
					ValidURI(title="Transcript source uri") ), required=True)
	srcjsonp = Variant((ValidTextLine(title="Transcript source jsonp"),
						ValidURI(title="Transcript source uri jsonp") ), required=False)
	lang = ValidTextLine(title="Transcript language", required=True, default='en')
	type = Choice(vocabulary=TRANSCRIPT_MIMETYPE_VOCABULARY, title='Transcript mimetype',
				  required=True, default=VTT_TRANSCRIPT_MIMETYPE)
	purpose = ValidTextLine(title="Transcript purpose", required=True, default='normal')

class INTIIDIdentifiable(interface.Interface):
	ntiid = ValidNTIID(title="Item NTIID", required=True)
	
class INTIMediaSource(IPresentationAsset):
	service = ValidTextLine(title="Source service", required=True)
	thumbnail = ValidTextLine(title="Source thumbnail", required=False)

class IVisible(interface.Interface):
	"""
	marker interface for things that have visibility
	"""
	visibility = Choice(vocabulary=VISIBILITY_VOCABULARY, title='Media ref visibility',
					 	required=False, default=EVERYONE)

class IMediaRef(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset, IVisible):
	pass

class INTIMedia(IDCDescriptiveProperties, INTIIDIdentifiable, ICreated, ITitled, IPresentationAsset):
	creator = ValidTextLine(title="Media creator", required=False)
	title = ValidTextLine(title="Media title", required=False, default=u'')
	description = ValidTextLine(title="Media description", required=False, default=u'')
	
class INTIVideoSource(INTIMediaSource):
	width = Int(title="Video width", required=False)
	height = Int(title="Video height", required=False)
	poster = ValidTextLine(title="Video poster", required=False)
	service = Choice(vocabulary=VIDEO_SERVICES_VOCABULARY, title='Video service',
					 required=True, default=HTML5_VIDEO_SERVICE)
	
	source = ListOrTuple(Variant((Choice(vocabulary=VIDEO_SOURCES_VOCABULARY), 
								  ValidTextLine())),
						 title='Video source', required=True, min_length=1)

	type = ListOrTuple(	Choice(vocabulary=VIDEO_SERVICE_TYPES_VOCABULARY),
						title='Video service types', required=True, min_length=1)
	
class INTIVideo(INTIMedia):	
	subtitle = Bool(title="Subtitle flag", required=False, default=None)
	
	closed_caption = Bool(title="Close caption flag", required=False, default=None)

	sources = ListOrTuple(value_type=Object(INTIVideoSource), 
						  title="The video sources", required=False, min_length=0)

	transcripts = ListOrTuple(value_type=Object(INTITranscript), 
							  title="The transcripts", required=False, min_length=0)

class INTIVideoRef(IMediaRef):
	label = ValidText(title="Video label", required=False)
	poster = ValidTextLine(title="Video poster", required=False)

class INTIAudioSource(INTIMediaSource):
	service = Choice(vocabulary=AUDIO_SERVICES_VOCABULARY, title='Audio service',
					 required=True, default=HTML5_AUDIO_SERVICE)

	source = ListOrTuple(Variant((Choice(vocabulary=AUDIO_SOURCES_VOCABULARY), 
								  ValidTextLine())),
						 title='Audio source', required=True, min_length=1)

	type = ListOrTuple(Choice(vocabulary=AUDIO_SERVICE_TYPES_VOCABULARY),
					   title='Audio service types', required=True, min_length=1)

class INTIAudio(INTIMedia):
	sources = ListOrTuple(value_type=Object(INTIAudioSource), 
						  title="The audio sources", required=False, min_length=1)

	transcripts = ListOrTuple(value_type=Object(INTITranscript), 
							  title="The transcripts", required=False, min_length=0)

class INTIAudioRef(IMediaRef):
	pass
	
class INTISlide(INTIIDIdentifiable, IPresentationAsset):
	slidevideoid = ValidNTIID(title="Slide video NTIID", required=True)
	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	slidevideostart = Number(title="Video start", required=False, default=0)
	slidevideoend = Number(title="Video end", required=False, default=0)
	slideimage = ValidTextLine(title="Slide image source", required=False)
	slidenumber = Int(title="Slide number", required=True, default=1)

class INTISlideVideo(IDCDescriptiveProperties, INTIIDIdentifiable, ICreated, ITitled, IPresentationAsset):
	video_ntiid = ValidNTIID(title="Slide video NTIID", required=True)
	creator = ValidTextLine(title="Slide video creator", required=True)
	title = ValidTextLine(title="Slide video title", required=False, default=u'')
	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	thumbnail = ValidTextLine(title="Slide video thumbnail", required=False)
	description = ValidTextLine(title="Slide video description", required=False)

class INTISlideDeck(IDCDescriptiveProperties, INTIIDIdentifiable, ICreated, ITitled, IPresentationAsset):
	Slides = IndexedIterable(value_type=Object(INTISlide), 
						 	 title="The slides", required=False, min_length=1)

	Videos = IndexedIterable(value_type=Object(INTISlideVideo), 
						 	 title="The slide videos", required=False, min_length=1)

	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	
	creator = ValidTextLine(title="Slide deck creator", required=True)
	title = ValidTextLine(title="Slide deck title", required=False, default=u'')
	description = ValidTextLine(title="Slide deck description", required=False)

class INTITimeline(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	label = ValidTextLine(title="The label", required=True, default=u'')
	href = ValidTextLine(title="Resource href", required=False, default=u'')
	icon = ValidTextLine(title="Icon href", required=False)
	description = ValidTextLine(title="Timeline description", required=False)
	suggested_inline = Bool("Suggested inline flag", required=False, default=False)

class INTIRelatedWorkRef(IGroupOverViewable, INTIIDIdentifiable, ICreated, IPresentationAsset, IVisible):
	href = ValidTextLine(title="Related work href", required=False, default=u'')
	target = ValidNTIID(title="Target NTIID", required=False)
	creator = ValidTextLine(title="The creator", required=False)
	section = ValidTextLine(title="Section", required=False)
	description = ValidText(title="Slide video description", required=False)
	icon = ValidTextLine(title="Related work icon href", required=False)
	type = ValidTextLine(title="The target mimetype", required=False)
	label = ValidTextLine(title="The label", required=False, default=u'')
	ntiid = Variant((ValidTextLine(title="Related content ntiid"),
					 ValidNTIID(title="Related content ntiid") ), required=True)
INTIRelatedWork = INTIRelatedWorkRef

class INTIBaseDiscussion(IGroupOverViewable, INTIIDIdentifiable, ITitled, IPresentationAsset):
	title = ValidTextLine(title="Discussion title", required=False)
	icon = ValidTextLine(title="Discussion icon href", required=False)
	label = ValidTextLine(title="The label", required=False, default=u'')
	ntiid = Variant((ValidTextLine(title="Discussion NTIID"),
					 ValidNTIID(title="Discussion NTIID") ), required=True)
	
class INTIDiscussionRef(INTIBaseDiscussion):
	target = Variant((ValidTextLine(title="Target NTIID"),
					  ValidNTIID(title="Target NTIID") ), required=True)

	def isCourseBundle():
		"""
		return if this DiscussionRef refers to a course bundle
		"""

class INTIAssessmentRef(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	ntiid = ValidNTIID(title="Discussion NTIID", required=True)
	target = ValidNTIID(title="Target NTIID", required=True)
	label = ValidTextLine(title="The label", required=False, default=u'')
IAssessmentRef = INTIAssessmentRef

class INTIQuestionSetRef(INTIAssessmentRef):
	question_count = Int(title="Question count", required=False)
IQuestionSetRef = INTIQuestionSetRef

class INTIQuestionRef(INTIAssessmentRef):
	pass
IQuestionRef = INTIQuestionRef

class INTIAssignmentRef(INTIAssessmentRef, ITitled):
	containerId = ValidNTIID(title="Container NTIID", required=True)
	title = ValidTextLine(title="Assignment title", required=False)
IAssignmentRef = INTIAssignment = INTIAssignmentRef

class INTICourseOverviewSpacer(IGroupOverViewable, INTIIDIdentifiable, IPresentationAsset):
	pass
	
class INTICourseOverviewGroup(ITitled, INTIIDIdentifiable, IPresentationAsset, 
							  IFiniteSequence, IIterable):
	ntiid = ValidNTIID(title="Overview NTIID", required=False)
	Items = IndexedIterable(value_type=Variant((Object(IGroupOverViewable),
												Object(IGroupOverViewableWeakRef))), 
						 	title="The overview items", required=False, min_length=0)
	title = ValidTextLine(title="Overview title", required=False)
	accentColor = ValidTextLine(title="Overview color", required=False)

class INTILessonOverview(ITitled, INTIIDIdentifiable, IPresentationAsset,
						 IFiniteSequence, IIterable):
	Items = IndexedIterable(value_type=Object(INTICourseOverviewGroup), 
						 	title="The overview items", required=False, min_length=0)
	title = ValidTextLine(title="Overview title", required=False)

class IPresentationVisibility(interface.Interface):
	"""
	marker interface to return the visibility for an object.
	
	Register as an adapter
	"""
	
	def visibility():
		pass
