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

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTIAudioRef
from .interfaces import INTIVideoRef

from .media import NTIAudioRef
from .media import NTIVideoRef

@component.adapter(INTIVideoRef)
@interface.implementer(INTIVideo)
def ntivideo_to_ntivideoref(video):
    result = NTIVideoRef(ntiid=video.ntiid,
                         poster=video.poster,
                         label=video.label)
    return result

@component.adapter(INTIAudioRef)
@interface.implementer(INTIAudio)
def ntiaudio_to_ntiaudioref(video):
    result = NTIAudioRef(ntiid=video.ntiid)
    return result
