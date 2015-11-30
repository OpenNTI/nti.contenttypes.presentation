#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from .media import NTIAudioRef
from .media import NTIVideoRef
from .media import NTIAudioRollRef
from .media import NTIVideoRollRef

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef
from .interfaces import INTIAudioRoll
from .interfaces import INTIVideoRoll
from .interfaces import INTIAudioRollRef
from .interfaces import INTIVideoRollRef

@component.adapter(INTIVideo)
@interface.implementer(INTIVideoRef)
def ntivideo_to_ntivideoref(video):
	result = NTIVideoRef(ntiid=video.ntiid,
						 target=video.ntiid,
						 poster=video.title,
						 label=video.title)
	result.byline = video.byline
	result.creator = video.creator
	return result

@component.adapter(INTIAudio)
@interface.implementer(INTIAudioRef)
def ntiaudio_to_ntiaudioref(audio):
	result = NTIAudioRef(ntiid=audio.ntiid,
						 target=audio.ntiid)
	result.byline = audio.byline
	result.creator = audio.creator
	return result

@component.adapter(INTIAudioRoll)
@interface.implementer(INTIAudioRollRef)
def ntiaudioroll_to_ntiaudiorollref(roll):
	result = NTIAudioRollRef(ntiid=roll.ntiid,
							 target=roll.ntiid)
	result.byline = roll.byline
	result.creator = roll.creator
	return result

@component.adapter(INTIVideoRoll)
@interface.implementer(INTIVideoRollRef)
def ntivideoroll_to_ntivideorollref(roll):
	result = NTIVideoRollRef(ntiid=roll.ntiid,
							 target=roll.ntiid)
	result.byline = roll.byline
	result.creator = roll.creator
	return result
