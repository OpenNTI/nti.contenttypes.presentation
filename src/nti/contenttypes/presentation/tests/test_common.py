#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import starts_with
from hamcrest import assert_that

import unittest
from datetime import datetime

from nti.contenttypes.presentation.common import generate_ntiid

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestCommon(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_generate_ntiid(self):
        ntiid = generate_ntiid('FOO', now=datetime.fromtimestamp(1000))
        assert_that(ntiid, starts_with(
            'tag:nextthought.com,2011-10:NTI-FOO-system_19691231181640_000000'))
