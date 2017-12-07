#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.contenttypes.presentation import NTI_TIMELINE
from nti.contenttypes.presentation import NTI_TIMELIME_REF

from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTITimelineRef

from nti.contenttypes.presentation.mixins import PersistentPresentationAsset
from nti.contenttypes.presentation.mixins import RecordablePresentationAsset

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

logger = __import__('logging').getLogger(__name__)


@total_ordering
@interface.implementer(INTITimeline)
class NTITimeLine(RecordablePresentationAsset):
    createDirectFieldProperties(INTITimeline)

    __external_class_name__ = "Timeline"
    mime_type = mimeType = 'application/vnd.nextthought.ntitimeline'

    target = None
    desc = alias('description')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(NTI_TIMELINE)
        return self.ntiid

    def __lt__(self, other):
        try:
            return (self.mimeType, self.label) < (other.mimeType, other.label)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.label) > (other.mimeType, other.label)
        except AttributeError:  # pragma: no cover
            return NotImplemented


@EqHash('target')
@interface.implementer(INTITimelineRef)
class NTITimeLineRef(PersistentPresentationAsset):  # not recordable
    createDirectFieldProperties(INTITimelineRef)

    __external_class_name__ = "TimelineRef"
    mime_type = mimeType = 'application/vnd.nextthought.ntitimelineref'

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(NTI_TIMELIME_REF)
        return self.ntiid
