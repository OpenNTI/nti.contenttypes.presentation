#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from itertools import chain
from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty
from zope.cachedescriptors.property import CachedProperty

from persistent.list import PersistentList

from nti.contenttypes.presentation import NTI_SLIDE
from nti.contenttypes.presentation import NTI_SLIDE_DECK
from nti.contenttypes.presentation import NTI_SLIDE_VIDEO
from nti.contenttypes.presentation import NTI_SLIDE_DECK_REF

from nti.contenttypes.presentation.interfaces import EVERYONE

from nti.contenttypes.presentation.interfaces import INTISlide
from nti.contenttypes.presentation.interfaces import INTISlideDeck
from nti.contenttypes.presentation.interfaces import INTISlideVideo
from nti.contenttypes.presentation.interfaces import INTISlideDeckRef

from nti.contenttypes.presentation.mixin import PersistentPresentationAsset
from nti.contenttypes.presentation.mixin import RecordablePresentationAsset

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties


@interface.implementer(INTISlide)
class NTISlide(RecordablePresentationAsset):
    createDirectFieldProperties(INTISlide)

    __external_class_name__ = "Slide"
    mime_type = mimeType = 'application/vnd.nextthought.slide'

    image = alias('slideimage')
    number = alias('slidenumber')
    video = alias('slidevideoid')
    slide_deck = deck = alias('slidedeckid')
    end = video_end = alias('slidevideoend')
    start = video_start = alias('slidevideostart')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(NTI_SLIDE)
        return self.ntiid


@interface.implementer(INTISlideVideo)
class NTISlideVideo(RecordablePresentationAsset):
    createDirectFieldProperties(INTISlideVideo)

    __external_class_name__ = "NTISlideVideo"
    mime_type = mimeType = 'application/vnd.nextthought.ntislidevideo'

    Creator = alias('creator')
    video = alias('video_ntiid')
    slide_deck = deck = alias('slidedeckid')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(NTI_SLIDE_VIDEO)
        return self.ntiid


@total_ordering
@interface.implementer(INTISlideDeck)
class NTISlideDeck(RecordablePresentationAsset):
    createDirectFieldProperties(INTISlideDeck)

    __external_class_name__ = "NTISlideDeck"
    mime_type = mimeType = 'application/vnd.nextthought.ntislidedeck'

    jsonschema = 'slidedeck'

    slides = alias('Slides')
    videos = alias('Videos')
    Creator = alias('creator')
    id = alias('slidedeckid')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(NTI_SLIDE_DECK)
        return self.ntiid

    @CachedProperty("lastModified")
    def Items(self):
        result = list(chain(self.slides or (), self.videos or ()))
        return result

    def append(self, item):
        item.__parent__ = self  # take owership
        if INTISlide.providedBy(item):
            if self.slides is None:
                self.slides = PersistentList()
            self.slides.append(item)
        elif INTISlideVideo.providedBy(item):
            if self.slides is None:
                self.videos = PersistentList()
            self.videos.append(item)
    add = append

    def remove(self, item):
        result = True
        try:
            if INTISlide.providedBy(item) and self.slides:
                self.slides.remove(item)
            elif INTISlideVideo.providedBy(item) and self.videos:
                self.videos.remove(item)
            else:
                result = False
        except (AttributeError, ValueError):
            result = False
        return result

    def __contains__(self, obj):
        ntiid = getattr(obj, 'ntiid', None) or str(obj)
        for item in self.Items:
            if item.ntiid == ntiid:
                return True
        return False

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:
            return NotImplemented


@EqHash('target')
@interface.implementer(INTISlideDeckRef)
class NTISlideDeckRef(PersistentPresentationAsset): # not recordable
    createDirectFieldProperties(INTISlideDeckRef)

    __external_class_name__ = "SlideDeckRef"
    mime_type = mimeType = 'application/vnd.nextthought.ntislideckref'

    __name__ = alias('ntiid')

    visibility = EVERYONE

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(NTI_SLIDE_DECK_REF)
        return self.ntiid
