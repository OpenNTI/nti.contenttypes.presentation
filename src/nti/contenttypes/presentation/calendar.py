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

from nti.contenttypes.presentation import NTI_CALENDAR_EVENT_REF

from nti.contenttypes.presentation.interfaces import INTICalendarEventRef

from nti.contenttypes.presentation.mixins import PersistentPresentationAsset

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.schema.fieldproperty import createDirectFieldProperties

logger = __import__('logging').getLogger(__name__)


@EqHash('target')
@interface.implementer(INTICalendarEventRef)
class NTICalendarEventRef(PersistentPresentationAsset):  # not recordable

    createDirectFieldProperties(INTICalendarEventRef)

    __external_class_name__ = "CalendarEventRef"
    mime_type = mimeType = 'application/vnd.nextthought.nticalendareventref'

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(NTI_CALENDAR_EVENT_REF)
        return self.ntiid
