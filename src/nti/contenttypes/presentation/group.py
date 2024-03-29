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

from persistent.list import PersistentList

from nti.contenttypes.presentation import MessageFactory as _

from nti.contenttypes.presentation import NTI_COURSE_OVERVIEW_GROUP

from nti.contenttypes.presentation.interfaces import INTIMediaRef
from nti.contenttypes.presentation.interfaces import IGroupOverViewable
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup

from nti.contenttypes.presentation.mixins import RecordablePresentationAsset

from nti.property.property import alias

from nti.recorder.mixins import RecordableContainerMixin

from nti.schema.fieldproperty import createDirectFieldProperties

logger = __import__('logging').getLogger(__name__)


class DuplicateReference(ValueError):

    msg = _(u'Cannot have two equal refs in the same group')

    def __init__(self):
        super(DuplicateReference, self).__init__(self.msg)


@total_ordering
@interface.implementer(INTICourseOverviewGroup)
class NTICourseOverViewGroup(RecordablePresentationAsset,
                             RecordableContainerMixin):
    createDirectFieldProperties(INTICourseOverviewGroup)

    __external_class_name__ = "CourseOverviewGroup"
    mime_type = mimeType = "application/vnd.nextthought.nticourseoverviewgroup"

    items = alias('Items')
    color = alias('accentColor')

    jsonschema = 'overviewgroup'

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(NTI_COURSE_OVERVIEW_GROUP)
        return self.ntiid

    def __getitem__(self, index):
        item = self.items[index]
        return item

    def __setitem__(self, index, item):
        assert IGroupOverViewable.providedBy(item)
        item.__parent__ = self  # take ownership
        self.items[index] = item

    def __len__(self):
        result = len(self.items or ())
        return result

    def __iter__(self):
        return iter(self.items or ())

    def __contains__(self, obj):
        ntiid = getattr(obj, 'ntiid', None) or str(obj)
        for item in self:
            if item.ntiid == ntiid:
                return True
        return False

    def _validate_insert(self, item):
        assert IGroupOverViewable.providedBy(item)
        # We do not allow duplicate refs in the same group, since clients
        # do not have access to media refs, only the underlying media obj.
        # This avoids confusion in some operations.
        if INTIMediaRef.providedBy(item):
            new_target = getattr(item, 'target', '')
            if new_target:
                for child in self:
                    if getattr(child, 'target', '') == new_target:
                        raise DuplicateReference()

    def append(self, item):
        self._validate_insert(item)
        item.__parent__ = self  # take ownership
        self.items = PersistentList() if self.items is None else self.items
        self.items.append(item)
    add = append

    def insert(self, index, item):
        # Remove from our list if it exists, and then insert at.
        self.remove(item)
        # Only validate after remove.
        self._validate_insert(item)
        if index is None or index >= len(self):
            # Default to append.
            self.append(item)
        else:
            item.__parent__ = self  # take ownership
            self.items.insert(index, item)

    def pop(self, index):
        return self.items.pop(index)

    def remove(self, item):
        try:
            self.items.remove(item)
            return True
        except (AttributeError, ValueError):
            pass
        return False

    def reset(self):
        result = len(self)
        if self.items:
            del self.items[:]
        return result
    clear = reset

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented
