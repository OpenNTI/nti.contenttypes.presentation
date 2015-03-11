#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six

from zope import component
from zope import interface

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.externalization import toExternalObject

from .interfaces import INTISlide

CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@component.adapter( INTISlide )
@interface.implementer( IExternalObject )
class _NTISlideRenderExternalObject(object):

    def __init__( self, slide ):
        self.slide = slide

    def _do_toExternalObject( self, extDict ):
        if CLASS in extDict:
            extDict['class'] = (extDict.pop(CLASS) or u'').lower()
        
        for name in ("slidevideostart", "slidevideoend", "slidenumber"):
            value = extDict.get(name)
            if value is not None and not isinstance(value, six.string_types):
                extDict[name] = str(value)

        return extDict

    def toExternalObject( self, *args, **kwargs ):
        extDict = toExternalObject( self.slide, name='')
        self._do_toExternalObject( extDict )
        return extDict
