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

from nti.contenttypes.presentation import POLL_REF_MIME_TYPES
from nti.contenttypes.presentation import SURVEY_REF_MIME_TYPES

from nti.contenttypes.presentation.assessment import NTIPollRef
from nti.contenttypes.presentation.assessment import NTISurveyRef

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

from nti.externalization.internalization import find_factory_for


class TestDatastructures(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_pollref(self):
        for mimeType in POLL_REF_MIME_TYPES:
            ext_obj = {
                "MimeType": mimeType
            }
            factory = find_factory_for(ext_obj)
            assert_that(factory, is_not(none()))
            assert_that(factory(), is_(NTIPollRef))

    def test_surveyref(self):
        for mimeType in SURVEY_REF_MIME_TYPES:
            ext_obj = {
                "MimeType": mimeType
            }
            factory = find_factory_for(ext_obj)
            assert_that(factory, is_not(none()))
            assert_that(factory(), is_(NTISurveyRef))