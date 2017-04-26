#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from functools import total_ordering

from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from zope.cachedescriptors.property import readproperty

from zope.container.contained import Contained

from zope.location.location import locate

from zope.mimetype.interfaces import IContentTypeAware

from ZODB.interfaces import IConnection

from zc.dict import OrderedDict

from persistent.list import PersistentList

from nti.contenttypes.presentation import NTI_LESSON_OVERVIEW
from nti.contenttypes.presentation import NTI_COURSE_OVERVIEW_SPACER
from nti.contenttypes.presentation import NTI_LESSON_COMPLETION_CONSTRAINT

from nti.contenttypes.presentation._base import PersistentPresentationAsset
from nti.contenttypes.presentation._base import RecordablePresentationAsset

from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTICourseOverviewSpacer
from nti.contenttypes.presentation.interfaces import ISurveyCompletionConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraints
from nti.contenttypes.presentation.interfaces import IAssignmentCompletionConstraint

from nti.coremetadata.interfaces import SYSTEM_USER_ID

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.ntiids.ntiids import get_parts
from nti.ntiids.ntiids import make_ntiid

from nti.property.property import alias

from nti.publishing.mixins import CalendarPublishableMixin

from nti.recorder.mixins import RecordableContainerMixin

from nti.schema.field import SchemaConfigured
from nti.schema.fieldproperty import createDirectFieldProperties


@interface.implementer(INTICourseOverviewSpacer)
class NTICourseOverViewSpacer(PersistentPresentationAsset): # not recordable
    createDirectFieldProperties(INTICourseOverviewSpacer)

    __external_class_name__ = u"CourseOverviewSpacer"
    mime_type = mimeType = u"application/vnd.nextthought.nticourseoverviewspacer"

    @readproperty
    def ntiid(self):
        result = self.generate_ntiid(NTI_COURSE_OVERVIEW_SPACER)
        self.ntiid = result
        return result


@total_ordering
@interface.implementer(INTILessonOverview)
class NTILessonOverView(CalendarPublishableMixin,
                        RecordableContainerMixin,
                        RecordablePresentationAsset):
    createDirectFieldProperties(INTILessonOverview)

    __external_class_name__ = u"LessonOverView"
    mime_type = mimeType = u"application/vnd.nextthought.ntilessonoverview"

    items = alias('Items')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):
        self.ntiid = self.generate_ntiid(NTI_LESSON_OVERVIEW)
        return self.ntiid

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, item):
        assert INTICourseOverviewGroup.providedBy(item)
        item.__parent__ = self  # take ownership
        self.items[index] = item

    def __len__(self):
        return len(self.items or ())

    def __iter__(self):
        return iter(self.items or ())

    def __contains__(self, obj):
        ntiid = getattr(obj, 'ntiid', None) or str(obj)
        for item in self:
            if item.ntiid == ntiid:
                return True
        return False

    def append(self, group):
        assert INTICourseOverviewGroup.providedBy(group)
        group.__parent__ = self  # take ownership
        self.items = PersistentList() if self.items is None else self.items
        self.items.append(group)
    add = append

    def insert(self, index, obj):
        # Remove from our list if it exists, and then insert at.
        self.remove(obj)
        if index is None or index >= len(self):
            # Default to append.
            self.append(obj)
        else:
            obj.__parent__ = self  # take ownership
            self.items.insert(index, obj)

    def pop(self, index):
        self.items.pop(index)

    def remove(self, group):
        try:
            self.items.remove(group)
            return True
        except (AttributeError, ValueError):
            pass
        return False

    def reset(self, *args, **kwargs):
        result = len(self)
        if self.items:
            del self.items[:]
        return result
    clear = reset

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


@component.adapter(INTILessonOverview, IContentTypeAware)
@interface.implementer(ILessonPublicationConstraints)
class LessonPublicationConstraints(PersistentCreatedModDateTrackingObject,
                                   OrderedDict):

    parameters = {}  # IContentTypeAware

    __external_class_name__ = u"LessonPublicationConstraints"
    mime_type = mimeType = u"application/vnd.nextthought.lesson.publicationconstraints"

    def _get_key(self):
        count = len(self)
        key = '%d' % count
        while key in self:
            count += 1
            key = '%d' % count
        return key

    def __setitem__(self, key, value):
        key = self._get_key()
        locate(value, self, key)
        OrderedDict.__setitem__(self, key, value)
        self.updateLastMod()

    def __delitem__(self, key):
        OrderedDict.__delitem__(self, key)
        self.updateLastMod()

    def append(self, item):
        self['ignore'] = item

    def extend(self, items):
        for item in items or ():
            self.append(item)

    @property
    def Items(self):
        return list(self.values())


@component.adapter(INTILessonOverview)
@interface.implementer(ILessonPublicationConstraints)
def constraints_for_lesson(lesson, create=True):
    constraints = None
    annotations = IAnnotations(lesson)
    try:
        KEY = 'LessonPublicationConstraints'
        constraints = annotations[KEY]
    except KeyError:
        if create:
            constraints = LessonPublicationConstraints()
            annotations[KEY] = constraints
            constraints.__name__ = KEY
            constraints.__parent__ = lesson
            connection = IConnection(lesson, None)
            if connection is not None:
                connection.add(constraints)
    return constraints


@interface.implementer(ILessonPublicationConstraint, IContentTypeAware)
class LessonCompletionConstraint(PersistentCreatedModDateTrackingObject,
                                 SchemaConfigured,
                                 Contained):

    parameters = {}  # IContentTypeAware
    creator = SYSTEM_USER_ID

    @readproperty
    def ntiid(self):
        lesson = getattr(self.__parent__, '__parent__', None)
        base_ntiid = getattr(lesson, 'ntiid', None)
        if base_ntiid and self.__name__:
            parts = get_parts(base_ntiid)
            specific = "%s.%s" % (parts.specific, self.__name__)
            result = make_ntiid(date=parts.date,
                                specific=specific,
                                provider=parts.provider,
                                nttype=NTI_LESSON_COMPLETION_CONSTRAINT)
            self.ntiid = result
            return result
        return None


@interface.implementer(IAssignmentCompletionConstraint)
class AssignmentCompletionConstraint(LessonCompletionConstraint):
    createDirectFieldProperties(IAssignmentCompletionConstraint)

    mime_type = mimeType = u"application/vnd.nextthought.lesson.assignmentcompletionconstraint"


@interface.implementer(ISurveyCompletionConstraint)
class SurveyCompletionConstraint(LessonCompletionConstraint):
    createDirectFieldProperties(ISurveyCompletionConstraint)

    mime_type = mimeType = u"application/vnd.nextthought.lesson.surveycompletionconstraint"

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
    "moved to nti.contenttypes.presentation.group",
    "nti.contenttypes.presentation.group",
    "NTICourseOverViewGroup")
