#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import instance_of

import unittest

from nti.contenttypes.presentation.group import NTICourseOverViewGroup
from nti.contenttypes.presentation.relatedwork import NTIRelatedWorkRef

from nti.contenttypes.presentation.wref import PresentationAssetWeakRef

from nti.wref.interfaces import IWeakRef

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestWref(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_adapter(self):
        for clazz in (NTICourseOverViewGroup, NTIRelatedWorkRef):
            asset = clazz()
            asset.ntiid = 'tag:nextthought.com,2011-10:NTI-FOO-system_19691231181640_000000'
            wref = IWeakRef(asset, None)
            assert_that(wref, is_not(none()))
            assert_that(wref, instance_of(PresentationAssetWeakRef))
