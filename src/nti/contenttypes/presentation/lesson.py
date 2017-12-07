#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from zope.cachedescriptors.property import readproperty

from zope.container.contained import Contained

from zope.container.ordered import OrderedContainer

from zope.deprecation import deprecated

from zope.mimetype.interfaces import IContentTypeAware

from ZODB.interfaces import IConnection

from persistent.list import PersistentList

from nti.containers.dicts import OrderedDict

from nti.contenttypes.presentation import NTI_LESSON_OVERVIEW
from nti.contenttypes.presentation import NTI_COURSE_OVERVIEW_SPACER
from nti.contenttypes.presentation import NTI_LESSON_COMPLETION_CONSTRAINT

from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import INTICourseOverviewSpacer
from nti.contenttypes.presentation.interfaces import ISurveyCompletionConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraints
from nti.contenttypes.presentation.interfaces import IAssignmentCompletionConstraint
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraintChecker

from nti.contenttypes.presentation.mixins import PersistentPresentationAsset
from nti.contenttypes.presentation.mixins import RecordablePresentationAsset

from nti.coremetadata.interfaces import SYSTEM_USER_ID

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.ntiids.ntiids import get_parts
from nti.ntiids.ntiids import make_ntiid

from nti.property.property import alias

from nti.publishing.mixins import CalendarPublishableMixin

from nti.recorder.mixins import RecordableContainerMixin

from nti.schema.field import SchemaConfigured
from nti.schema.fieldproperty import createDirectFieldProperties

from nti.traversal.traversal import find_interface

logger = __import__('logging').getLogger(__name__)


@interface.implementer(INTICourseOverviewSpacer)
class NTICourseOverViewSpacer(PersistentPresentationAsset):  # not recordable
    createDirectFieldProperties(INTICourseOverviewSpacer)

    __external_class_name__ = "CourseOverviewSpacer"
    mime_type = mimeType = "application/vnd.nextthought.nticourseoverviewspacer"

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        result = self.generate_ntiid(NTI_COURSE_OVERVIEW_SPACER)
        self.ntiid = result
        return result


@total_ordering
@interface.implementer(INTILessonOverview)
class NTILessonOverView(CalendarPublishableMixin,
                        RecordableContainerMixin,
                        RecordablePresentationAsset):
    createDirectFieldProperties(INTILessonOverview)

    __external_class_name__ = "LessonOverView"
    mime_type = mimeType = "application/vnd.nextthought.ntilessonoverview"

    items = alias('Items')

    __name__ = alias('ntiid')

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
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
        return self.items.pop(index)

    def remove(self, group):
        try:
            self.items.remove(group)
            return True
        except (AttributeError, ValueError):
            pass
        return False

    def reset(self, *unused_args, **unused_kwargs):
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


deprecated("LessonPublicationConstraints", "use new storage")
class LessonPublicationConstraints(PersistentCreatedModDateTrackingObject,
                                   OrderedDict):
    pass


@component.adapter(INTILessonOverview, IContentTypeAware)
@interface.implementer(ILessonPublicationConstraints)
class LessonConstraintContainer(PersistentCreatedModDateTrackingObject,
                                OrderedContainer):

    parameters = {}  # IContentTypeAware

    __external_class_name__ = "LessonPublicationConstraints"
    mime_type = mimeType = "application/vnd.nextthought.lesson.publicationconstraints"

    def _get_key(self):
        count = len(self)
        key = '%d' % count
        while key in self:
            count += 1
            key = '%d' % count
        return key

    def __setitem__(self, unused_key, value):
        key = self._get_key()
        OrderedContainer.__setitem__(self, key, value)
        self.updateLastMod()

    def __delitem__(self, key):
        OrderedContainer.__delitem__(self, key)
        self.updateLastMod()

    def append(self, item):
        self['ignore'] = item

    def extend(self, items):
        for item in items or ():
            self.append(item)

    def clear(self):
        for key in list(self.keys()):
            del self[key]

    @property
    def Items(self):
        return list(self.values())


CONSTRAINT_ANNOTATION_KEY = 'LessonPublicationConstraints'


@component.adapter(INTILessonOverview)
@interface.implementer(ILessonPublicationConstraints)
def constraints_for_lesson(lesson, create=True):
    constraints = None
    annotations = IAnnotations(lesson)
    try:
        constraints = annotations[CONSTRAINT_ANNOTATION_KEY]
    except KeyError:
        if create:
            constraints = LessonConstraintContainer()
            annotations[CONSTRAINT_ANNOTATION_KEY] = constraints
            constraints.__name__ = CONSTRAINT_ANNOTATION_KEY
            constraints.__parent__ = lesson
            connection = IConnection(lesson, None)
            if connection is not None:
                # pylint: disable=too-many-function-args
                connection.add(constraints)
    return constraints


@interface.implementer(ILessonPublicationConstraint, IContentTypeAware)
class LessonCompletionConstraint(PersistentCreatedModDateTrackingObject,
                                 SchemaConfigured,
                                 Contained):

    parameters = {}  # IContentTypeAware
    creator = SYSTEM_USER_ID

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        lesson = find_interface(self, INTILessonOverview, strict=False)
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

    mime_type = mimeType = "application/vnd.nextthought.lesson.assignmentcompletionconstraint"


@interface.implementer(ISurveyCompletionConstraint)
class SurveyCompletionConstraint(LessonCompletionConstraint):
    createDirectFieldProperties(ISurveyCompletionConstraint)

    mime_type = mimeType = "application/vnd.nextthought.lesson.surveycompletionconstraint"


def get_constraint_satisfied_time(context, lesson):
    satisfied_time = None
    constraints = constraints_for_lesson(lesson, False)
    if constraints is not None:
        satisfied_time = 0
        for constraint in constraints.Items or ():
            checker = ILessonPublicationConstraintChecker(constraint, None)
            if checker is not None:
                # pylint: disable=too-many-function-args
                constraint_satisfied_time = checker.satisfied_time(context)
                if constraint_satisfied_time is not None:
                    satisfied_time = max(satisfied_time,
                                         constraint_satisfied_time)
                else:
                    # If we have a constraint that does not return a time,
                    # it is not satisfied, and we should break out of the
                    # loop and return None because not all constraints have
                    # been satisfied for this lesson.
                    satisfied_time = None
                    break
    return satisfied_time


import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
    "moved to nti.contenttypes.presentation.group",
    "nti.contenttypes.presentation.group",
    "NTICourseOverViewGroup")
