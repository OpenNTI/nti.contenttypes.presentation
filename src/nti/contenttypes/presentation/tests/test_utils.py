#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest
import importlib

from nti.contenttypes.presentation import AUDIO_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_MIME_TYPES
from nti.contenttypes.presentation import POLL_REF_MIME_TYPES
from nti.contenttypes.presentation import TIMELINE_MIME_TYPES
from nti.contenttypes.presentation import AUDIO_REF_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_REF_MIME_TYPES
from nti.contenttypes.presentation import AUDIO_ROLL_MIME_TYPES
from nti.contenttypes.presentation import SURVEY_REF_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_ROLL_MIME_TYPES
from nti.contenttypes.presentation import QUESTION_REF_MIME_TYPES
from nti.contenttypes.presentation import TIMELINE_REF_MIME_TYPES
from nti.contenttypes.presentation import ASSIGNMENT_REF_MIME_TYPES
from nti.contenttypes.presentation import DISCUSSION_REF_MIME_TYPES
from nti.contenttypes.presentation import SLIDE_DECK_REF_MIME_TYPES
from nti.contenttypes.presentation import LESSON_OVERVIEW_MIME_TYPES
from nti.contenttypes.presentation import QUESTIONSET_REF_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_MIME_TYPES
from nti.contenttypes.presentation import COURSE_OVERVIEW_GROUP_MIME_TYPES

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestUtils(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def mime_types(self):
        for data in (AUDIO_MIME_TYPES,
                     VIDEO_MIME_TYPES,
                     POLL_REF_MIME_TYPES,
                     TIMELINE_MIME_TYPES,
                     AUDIO_REF_MIME_TYPES,
                     VIDEO_REF_MIME_TYPES,
                     AUDIO_ROLL_MIME_TYPES,
                     SURVEY_REF_MIME_TYPES,
                     VIDEO_ROLL_MIME_TYPES,
                     QUESTION_REF_MIME_TYPES,
                     TIMELINE_REF_MIME_TYPES,
                     ASSIGNMENT_REF_MIME_TYPES,
                     DISCUSSION_REF_MIME_TYPES,
                     SLIDE_DECK_REF_MIME_TYPES,
                     LESSON_OVERVIEW_MIME_TYPES,
                     QUESTIONSET_REF_MIME_TYPES,
                     RELATED_WORK_REF_MIME_TYPES,
                     COURSE_OVERVIEW_GROUP_MIME_TYPES):
            yield data

    def test_creators(self):
        mod_name = 'nti.contenttypes.presentation.utils'
        module = importlib.import_module(mod_name)
        for data in self.mime_types():
            found = False
            for mimeType in data:
                s = mimeType[mimeType.rindex('.') + 1:]
                func = 'create_%s_from_external' % s
                if func in module.__dict__:
                    found = True
                    break
            assert_that(found, is_(True), data)

    def test_prehooks(self):
        mod_name = 'nti.contenttypes.presentation.internalization'
        module = importlib.import_module(mod_name)
        for data in self.mime_types():
            found = False
            for mimeType in data:
                s = mimeType[mimeType.rindex('.') + 1:]
                func = 'internalization_%s_pre_hook' % s
                if func in module.__dict__:
                    found = True
                    break
            assert_that(found, is_(True), data)
