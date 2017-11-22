#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import contains
from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than

import os
import unittest

import simplejson

from nti.contenttypes.presentation import LESSON_OVERVIEW_MIME_TYPES
from nti.contenttypes.presentation import COURSE_OVERVIEW_GROUP_MIME_TYPES

from nti.contenttypes.presentation.datastructures import legacy_ntilessonoverview_transform
from nti.contenttypes.presentation.datastructures import legacy_nticourseoverviewgroup_transform

from nti.contenttypes.presentation.group import NTICourseOverViewGroup

from nti.contenttypes.presentation.lesson import NTILessonOverView

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import find_factory_for

ITEMS = StandardExternalFields.ITEMS
MIMETYPE = StandardExternalFields.MIMETYPE


class TestDatastructures(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_factory(self):
        for mimeType in COURSE_OVERVIEW_GROUP_MIME_TYPES:
            ext_obj = {
                MIMETYPE: mimeType
            }
            factory = find_factory_for(ext_obj)
            assert_that(factory, is_not(none()))
            assert_that(factory(), is_(NTICourseOverViewGroup))

        for mimeType in LESSON_OVERVIEW_MIME_TYPES:
            ext_obj = {
                MIMETYPE: mimeType
            }
            factory = find_factory_for(ext_obj)
            assert_that(factory, is_not(none()))
            assert_that(factory(), is_(NTILessonOverView))

    def test_courseoverviewgroup_transform(self):
        path = os.path.join(os.path.dirname(__file__),
                            'courseoverviewgroup.json')
        with open(path, "r") as fp:
            ext_obj = simplejson.load(fp)
        old_length = len(ext_obj.get(ITEMS) or ())
        legacy_nticourseoverviewgroup_transform(ext_obj)
        items = ext_obj.get(ITEMS)
        assert_that(items,
                    has_length(greater_than(old_length)))

    def test_lessongroup_transform(self):
        path = os.path.join(os.path.dirname(__file__),
                            'lessonoverview.json')
        with open(path, "r") as fp:
            ext_obj = simplejson.load(fp)
        legacy_ntilessonoverview_transform(ext_obj)
        groups = ext_obj.get(ITEMS)
        assert_that(groups, has_length(5))

        assert_that(groups[0],
                    has_entry(ITEMS,
                              contains(has_entry(MIMETYPE, 'application/vnd.nextthought.ntivideoref'))))

        assert_that(groups[1],
                    has_entry(ITEMS,
                              contains(has_entry(MIMETYPE, 'application/vnd.nextthought.discussionref'))))

        assert_that(groups[2],
                    has_entry(ITEMS,
                              contains(has_entry(MIMETYPE, 'application/vnd.nextthought.assignmentref'))))

        assert_that(groups[3],
                    has_entry(ITEMS,
                              contains(has_entry(MIMETYPE, 'application/vnd.nextthought.questionsetref'))))

        assert_that(groups[4],
                    has_entry(ITEMS,
                              contains(has_entry(MIMETYPE, 'application/vnd.nextthought.relatedworkref'))))
