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
from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.externalization import toExternalObject

from .interfaces import INTIAudio
from .interfaces import INTIVideo

CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@interface.implementer( IExternalObject )
class _NTIMediaRenderExternalObject(object):

    def __init__( self, media ):
        self.media = media

    def _do_toExternalObject( self, extDict ):
        if MIMETYPE in extDict:
            extDict[StandardExternalFields.CTA_MIMETYPE] = extDict.pop(MIMETYPE)
            
        if CREATOR in extDict:
            extDict['creator'] = extDict.pop(CREATOR)
        
        for name in (CLASS, u'DCDescription', u'DCTitle', NTIID):
            extDict.pop(name, None)
     
        for source in extDict.get('sources') or ():
            source.pop(MIMETYPE, None)
            source.pop(StandardExternalFields.CLASS, None)
        
        for transcript in extDict.get('transcripts') or ():
            transcript.pop(MIMETYPE, None)
            transcript.pop(StandardExternalFields.CLASS, None)
        
        return extDict

    def toExternalObject( self, *args, **kwargs ):
        extDict = toExternalObject( self.media, name='')
        self._do_toExternalObject( extDict )
        return extDict

@component.adapter( INTIVideo )
class _NTIVideoRenderExternalObject(_NTIMediaRenderExternalObject):
    def _do_toExternalObject( self, extDict ):
        extDict = super(_NTIVideoRenderExternalObject, self)._do_toExternalObject(extDict)
        if 'closed_caption' in extDict:
            extDict['closedCaptions'] = extDict.pop('closed_caption')
        if 'subtitle' in extDict and extDict['subtitle'] is None:
            del extDict['subtitle']
        return extDict

@component.adapter( INTIAudio )
class _NTIAudioRenderExternalObject(_NTIMediaRenderExternalObject):
    pass
