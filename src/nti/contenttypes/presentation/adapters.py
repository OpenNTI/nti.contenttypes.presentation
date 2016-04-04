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

from nti.contenttypes.presentation.interfaces import INTIAudio
from nti.contenttypes.presentation.interfaces import INTIVideo
from nti.contenttypes.presentation.interfaces import INTIAudioRef
from nti.contenttypes.presentation.interfaces import INTIVideoRef
from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTITimelineRef
from nti.contenttypes.presentation.interfaces import INTISlideDeckRef

from nti.contenttypes.presentation.media import NTIAudioRef
from nti.contenttypes.presentation.media import NTIVideoRef

from nti.contenttypes.presentation.slide import NTISlideDeckRef

from nti.contenttypes.presentation.timeline import NTITimeLineRef

@component.adapter(INTIVideo)
@interface.implementer(INTIVideoRef)
def ntivideo_to_ntivideoref(video):
	result = NTIVideoRef(target=video.ntiid,
						 poster=video.title,
						 label=video.title)
	result.byline = video.byline
	result.creator = video.creator
	return result

@component.adapter(INTIAudio)
@interface.implementer(INTIAudioRef)
def ntiaudio_to_ntiaudioref(audio):
	result = NTIAudioRef(target=audio.ntiid)
	result.byline = audio.byline
	result.creator = audio.creator
	return result

@component.adapter(INTISlideDeck)
@interface.implementer(INTISlideDeckRef)
def slideck_to_ntislideckref(slideck):
	result = NTISlideDeckRef(target=slideck.ntiid)
	result.byline = slideck.byline
	result.creator = slideck.creator
	return result

@component.adapter(INTITimeline)
@interface.implementer(INTITimelineRef)
def timeline_to_ntitimelineref(timeline):
	result = NTITimeLineRef(target=timeline.ntiid)
	result.byline = timeline.byline
	result.creator = timeline.creator
	return result
