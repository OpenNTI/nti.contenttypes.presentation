#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

import unittest

from zope import interface

from nti.base.interfaces import IFile

from nti.contenttypes.presentation.media import NTITranscript

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestMedia(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_transcript(self):

        @interface.implementer(IFile)
        class Foo(object):
            __parent__ = None

        foo = Foo()
        transcript = NTITranscript()
        transcript.src = foo

        assert_that(foo, has_property('__parent__', is_(transcript)))
        assert_that(transcript.is_source_attached(), is_(True))
