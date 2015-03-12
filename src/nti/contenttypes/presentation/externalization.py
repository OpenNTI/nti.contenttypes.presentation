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

from nti.common.property import alias

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.externalization import toExternalObject
from nti.externalization.interfaces import StandardExternalFields

from .interfaces import INTIAudio
from .interfaces import INTIVideo
from .interfaces import INTISlide
from .interfaces import INTITimeline
from .interfaces import INTISlideDeck
from .interfaces import INTIDiscussion
from .interfaces import INTISlideVideo
from .interfaces import INTIRelatedWork
from .interfaces import INTIAssignmentRef

from . import NTI_SLIDE_DECK

CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
CREATOR = StandardExternalFields.CREATOR
MIMETYPE = StandardExternalFields.MIMETYPE

@interface.implementer( IExternalObject )
class _NTIBaseRenderExternalObject(object):

	def __init__( self, obj ):
		self.obj = obj

	def _do_toExternalObject( self, extDict ):
		return extDict

	def toExternalObject( self, *args, **kwargs ):
		extDict = toExternalObject( self.obj, name='')
		self._do_toExternalObject( extDict )
		return extDict

@interface.implementer( IExternalObject )
class _NTIMediaRenderExternalObject(_NTIBaseRenderExternalObject):

	media = alias('obj')
	
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

@interface.implementer( IExternalObject )
class _NTIBaseSlideExternalObject(_NTIBaseRenderExternalObject):

	slide = alias('obj')
	
	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict['class'] = (extDict.pop(CLASS) or u'').lower()
		
		if CREATOR in extDict:
			extDict['creator'] = extDict.pop(CREATOR)

		if 'description' in extDict and not extDict['description']:
			extDict.pop('description') 

		return extDict

@component.adapter( INTISlide )
class _NTISlideRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject( self, extDict ):
		super(_NTISlideRenderExternalObject, self)._do_toExternalObject(extDict)

		for name in ("slidevideostart", "slidevideoend", "slidenumber"):
			value = extDict.get(name)
			if value is not None and not isinstance(value, six.string_types):
				extDict[name] = str(value)

		return extDict

@component.adapter( INTISlideVideo )
class _NTISlideVideoRenderExternalObject(_NTIBaseSlideExternalObject):

	def _do_toExternalObject( self, extDict ):
		super(_NTISlideVideoRenderExternalObject, self)._do_toExternalObject(extDict)
			
		if 'video_ntiid' in extDict:
			extDict['video-ntiid'] = extDict.pop('video_ntiid') 

		return extDict

@component.adapter( INTISlideDeck )
class _NTISlideDeckRenderExternalObject(_NTIBaseSlideExternalObject):

	def toExternalObject( self, *args, **kwargs ):
		extDict = LocatedExternalDict()
		extDict['title'] = self.slide.title
		extDict['ntiid'] = self.slide.ntiid
		extDict['creator'] = self.slide.creator
		extDict[MIMETYPE] = self.slide.mimeType
		extDict['class'] = NTI_SLIDE_DECK.lower()
		extDict['slidedeckid'] = self.slide.slidedeckid
		extDict['Slides'] = [toExternalObject(x, name='render') for x in self.slide.slides]
		extDict['Videos'] = [toExternalObject(x, name='render') for x in self.slide.videos]
		return extDict

@component.adapter( INTITimeline )
class _NTITimelineRenderExternalObject(_NTIBaseRenderExternalObject):

	timeline = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if 'description' in extDict:
			extDict['desc'] = extDict.pop('description')
		return extDict
		
@component.adapter( INTIRelatedWork )
class _NTIRelatedWorkRenderExternalObject(_NTIBaseRenderExternalObject):

	related = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if CREATOR in extDict:
			extDict['creator'] = extDict.pop(CREATOR)
		if 'description' in extDict:
			extDict['desc'] = extDict.pop('description')
		if 'target' in extDict:
			extDict['target-ntiid'] = extDict.pop('target')
		if 'type' in extDict:
			extDict['targetMimeType'] = extDict['type']
		extDict["visibility"] = "everyone"
		return extDict

@component.adapter( INTIDiscussion )
class _NTIDiscussionRenderExternalObject(_NTIBaseRenderExternalObject):

	related = alias('obj')

	def _do_toExternalObject( self, extDict ):
		if CLASS in extDict:
			extDict.pop(CLASS)
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		return extDict

@component.adapter( INTIAssignmentRef )
class _NTIAssignmentRefRenderExternalObject(_NTIBaseRenderExternalObject):

	assignment = alias('obj')

	def _do_toExternalObject( self, extDict ):
		extDict[CLASS] = 'Assignment' # for legacy iPad
		extDict[MIMETYPE] = 'application/vnd.nextthought.assessment.assignment'  # for legacy iPad
		if 'ntiid' in extDict:
			extDict[NTIID] = extDict.pop('ntiid')
		if 'target' in extDict:
			extDict['Target-NTIID'] = extDict.pop('target')
		if 'containerId' in extDict:
			extDict['ContainerId'] = extDict.pop('containerId')
		return extDict
