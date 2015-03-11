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

from nti.externalization.interfaces import IExternalObject
from nti.externalization.externalization import toExternalObject

from .interfaces import INTIVideo

@interface.implementer( IExternalObject )
class _NTIMediaRenderExternalObject(object):

    def __init__( self, media ):
        self.media = media

    def _do_toExternalObject( self, extDict ):
        return extDict

    def toExternalObject( self, *args, **kwargs ):
        extDict = toExternalObject( self.media )
        self._do_toExternalObject( extDict )
        return extDict

@component.adapter( INTIVideo )
class _NTIVideoRenderExternalObject(_NTIMediaRenderExternalObject):
    pass
