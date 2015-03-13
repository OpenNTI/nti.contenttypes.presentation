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

from .interfaces import INTIVideo
from .interfaces import INTIVideoRef

from .media import NTIVideoRef

@component.adapter(INTIVideoRef)
@interface.implementer(INTIVideo)
def ntivideo_to_ntivideoref(video):
    result = NTIVideoRef(ntiid=video.ntiid,
                         poster=video.poster,
                         label=video.label)
    return result
