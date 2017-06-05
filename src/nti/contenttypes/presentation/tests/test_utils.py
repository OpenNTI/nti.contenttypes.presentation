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

from nti.contenttypes.presentation.utils import mime_types

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestUtils(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_creators(self):
        mod_name = 'nti.contenttypes.presentation.utils'
        module = importlib.import_module(mod_name)
        for data in mime_types():
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
        for data in mime_types():
            found = False
            for mimeType in data:
                s = mimeType[mimeType.rindex('.') + 1:]
                func = 'internalization_%s_pre_hook' % s
                if func in module.__dict__:
                    found = True
                    break
            assert_that(found, is_(True), data)
