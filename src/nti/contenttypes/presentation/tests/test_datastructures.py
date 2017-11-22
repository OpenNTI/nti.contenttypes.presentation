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
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than

import os
import unittest

import simplejson

from nti.contenttypes.presentation import COURSE_OVERVIEW_GROUP_MIME_TYPES

from nti.contenttypes.presentation.datastructures import legacy_nticourseoverviewgroup_transform

from nti.contenttypes.presentation.group import NTICourseOverViewGroup

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import find_factory_for

ITEMS = StandardExternalFields.ITEMS


class TestDatastructures(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_factory(self):
        for mimeType in COURSE_OVERVIEW_GROUP_MIME_TYPES:
            ext_obj = {
                "MimeType": mimeType
            }
            factory = find_factory_for(ext_obj)
            assert_that(factory, is_not(none()))
            assert_that(factory(), is_(NTICourseOverViewGroup))

    def test_internal(self):
        path = os.path.join(os.path.dirname(__file__),
                            'courseoverviewgroup.json')
        with open(path, "r") as fp:
            ext_obj = simplejson.load(fp)
        old_length = len(ext_obj.get(ITEMS) or ())
        legacy_nticourseoverviewgroup_transform(ext_obj)
        items = ext_obj.get(ITEMS)
        assert_that(items,
                    has_length(greater_than(old_length)))
