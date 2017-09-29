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
from hamcrest import assert_that

import unittest

from nti.contenttypes.presentation.discussion import NTIDiscussionRef

from nti.externalization.internalization import find_factory_for

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


@unittest.SkipTest
class TestDatastructures(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_legacy_discussion(self):
        ext_obj = {
            "MimeType": "application/vnd.nextthought.discussion",
        }
        factory = find_factory_for(ext_obj)
        assert_that(factory, is_not(none()))
        assert_that(factory, is_(NTIDiscussionRef))