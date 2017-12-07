#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,too-many-function-args

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraints
from nti.contenttypes.presentation.interfaces import IAssignmentCompletionConstraint

from nti.contenttypes.presentation.lesson import NTILessonOverView
from nti.contenttypes.presentation.lesson import LessonConstraintContainer
from nti.contenttypes.presentation.lesson import AssignmentCompletionConstraint

from nti.externalization.externalization import to_external_object

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestLesson(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    ntiid = u"tag:nextthought.com,2011-10:OU-NAQ-BIO"

    def test_constraints(self):
        constraints = LessonConstraintContainer()
        assert_that(constraints,
                    validly_provides(ILessonPublicationConstraints))
        assert_that(constraints,
                    verifiably_provides(ILessonPublicationConstraints))

    def test_assignment_completion_constraint(self):
        constraint = AssignmentCompletionConstraint(assignments=[self.ntiid])
        assert_that(constraint,
                    validly_provides(IAssignmentCompletionConstraint))
        assert_that(constraint,
                    verifiably_provides(IAssignmentCompletionConstraint))

    def test_io(self):
        constraints = LessonConstraintContainer()
        constraint = AssignmentCompletionConstraint(assignments=[self.ntiid])
        constraints.append(constraint)
        assert_that(constraint, has_property('__name__', is_not(none())))

        ext_obj = to_external_object(constraints)
        assert_that(ext_obj,
                    has_entries('MimeType', 'application/vnd.nextthought.lesson.publicationconstraints',
                                'Items', has_length(1)))

        factory = find_factory_for(ext_obj)
        assert_that(factory, is_not(none()))

        new_constraints = factory()
        update_from_external_object(new_constraints, ext_obj)
        assert_that(new_constraints, has_property('Items', has_length(1)))
        new_constraint = new_constraints.Items[0]
        assert_that(new_constraint, has_property('__name__', is_not(none())))
        assert_that(new_constraint,
                    has_property('assignments', is_(["tag:nextthought.com,2011-10:OU-NAQ-BIO"])))

    def test_adapter(self):
        lesson = NTILessonOverView()
        lesson.ntiid = u"tag:nextthought.com,2011-10:OU-NTILessonOverview-BIO"
        constraints = ILessonPublicationConstraints(lesson, None)
        assert_that(constraints, is_not(none()))
        constraint = AssignmentCompletionConstraint(assignments=[self.ntiid])
        constraints.append(constraint)
        assert_that(constraints, has_length(1))
        assert_that(constraint,
                    has_property('ntiid', is_("tag:nextthought.com,2011-10:OU-NTILessonCompletionConstraint-BIO.0")))
