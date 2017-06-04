#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_key
from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import starts_with

import unittest
from datetime import datetime

from nti.contenttypes.presentation.common import generate_ntiid

from nti.contenttypes.presentation.relatedwork import NTIRelatedWorkRef

from nti.externalization.externalization import to_external_object

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestCommon(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_generate_ntiid(self):
        ntiid = generate_ntiid(u'FOO', now=datetime.fromtimestamp(1000))
        assert_that(ntiid,
                    starts_with('tag:nextthought.com,2011-10:NTI-FOO-system_19691231181640_000000'))

    def test_related_work_ref_externalizes(self):

        related_work_ref = NTIRelatedWorkRef()
        related_work_ref.nti_requirements = u'requirement'

        ext_obj = to_external_object(related_work_ref)
        assert_that(ext_obj, has_entry('nti_requirements', 'requirement'))
        assert_that(ext_obj, has_key('byline'))
        assert_that(ext_obj, has_key('section'))
        assert_that(ext_obj, has_key('description'))
        assert_that(ext_obj, has_key('type'))
        assert_that(ext_obj, has_key('ntiid'))
        assert_that(ext_obj, has_key('target'))
