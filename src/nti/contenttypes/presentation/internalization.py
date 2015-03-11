#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

from zope import interface
from zope import component

from nti.common.string import map_string_adjuster

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.interfaces import IInternalObjectUpdater
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTISlide
from .interfaces import INTISlideVideo

CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@interface.implementer(IInternalObjectUpdater)
class _NTIMediaUpdater(InterfaceObjectIO):

	def fixCreator(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')
		return self
	
	def parseTranscripts(self, parsed):
		transcripts = parsed.get('transcripts')
		for idx, transcript in enumerate(transcripts or ()):
			if MIMETYPE not in transcript:
				transcript[MIMETYPE] = u'application/vnd.nextthought.ntitranscript'
			obj = find_factory_for(transcript)()
			transcripts[idx] = update_from_external_object(obj, transcript)
		return self
		
	def fixAll(self, parsed):
		self.fixCreator(parsed).parseTranscripts(parsed)
		return parsed
	
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTIMediaUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTIVideo)
class _NTIVideoUpdater(_NTIMediaUpdater):

	_ext_iface_upper_bound = INTIVideo

	def parseSources(self, parsed):
		sources = parsed.get('sources')
		for idx, source in enumerate(sources or ()):
			if MIMETYPE not in source:
				source[MIMETYPE] = u'application/vnd.nextthought.ntivideosource'
			obj = find_factory_for(source)()
			sources[idx] = update_from_external_object(obj, source)
		return self

	def fixCloseCaption(self, parsed):
		if 'closedCaptions' in parsed:
			parsed['closed_caption'] = parsed['closedCaptions']
		elif 'closedCaption' in parsed:
			parsed['closed_caption'] = parsed['closedCaption']
		return self
	
	def fixAll(self, parsed):
		self.parseSources(parsed).parseTranscripts(parsed).fixCloseCaption(parsed).fixCreator(parsed)
		return parsed

@component.adapter(INTIAudio)
class _NTIAudioUpdater(_NTIMediaUpdater):

	_ext_iface_upper_bound = INTIAudio

	def parseSources(self, parsed):
		sources = parsed.get('sources')
		for idx, source in enumerate(sources or ()):
			if MIMETYPE not in source:
				source[MIMETYPE] = u'application/vnd.nextthought.ntiaudiosource'
			obj = find_factory_for(source)()
			sources[idx] = update_from_external_object(obj, source)
		return self

	def fixAll(self, parsed):
		self.fixCreator(parsed).parseSources(parsed).parseTranscripts(parsed)
		return parsed

@component.adapter(INTISlide)
@interface.implementer(IInternalObjectUpdater)
class _NTISlideUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTISlide
	
	def fixAll(self, parsed):
		for name, func in ( ("slidevideostart", float),
							("slidevideoend", float),
							("slidenumber", int)):
			
			value = parsed.get(name, None)
			if value is not None and isinstance(value, six.string_types):
				try:
					parsed[name] = func(value) 
				except (TypeError, ValueError):
					pass
		return self
		
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTISlideUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result

@component.adapter(INTISlideVideo)
@interface.implementer(IInternalObjectUpdater)
class _NTISlideVideoUpdater(InterfaceObjectIO):
	
	_ext_iface_upper_bound = INTISlideVideo
	
	def fixAll(self, parsed):
		if 'creator' in parsed:
			parsed[CREATOR] = parsed.pop('creator')
		
		if 'video-ntiid' in parsed:
			parsed['video_ntiid'] = parsed.pop('video-ntiid')

		return self
		
	def updateFromExternalObject(self, parsed, *args, **kwargs):
		self.fixAll(map_string_adjuster(parsed))
		result = super(_NTISlideVideoUpdater,self).updateFromExternalObject(parsed, *args, **kwargs)
		return result
