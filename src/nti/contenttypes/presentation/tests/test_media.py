#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

import unittest

from zope import interface

from nti.base.interfaces import IFile

from nti.contenttypes.presentation.interfaces import ITranscriptContainer 

from nti.contenttypes.presentation.media import NTIVideo
from nti.contenttypes.presentation.media import NTITranscript

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer

from nti.externalization.externalization import to_external_object


class TestMedia(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_transcript(self):

        @interface.implementer(IFile)
        class Foo(object):
            __parent__ = None
            data = b'data'
            contentType = 'text/vtt'

        foo = Foo()
        transcript = NTITranscript()
        transcript.src = foo

        assert_that(foo, has_property('__parent__', is_(transcript)))
        assert_that(transcript.is_source_attached(), is_(True))

        result = to_external_object(transcript, name='exporter')
        assert_that(result,
                    has_entries('contents', is_not(none()),
                                'contentType', is_('text/vtt')))

    def test_container(self):
        video = NTIVideo()
        transcript = NTITranscript()

        container = ITranscriptContainer(video, None)
        assert_that(container, is_not(none()))
        assert_that(container, validly_provides(ITranscriptContainer))
        assert_that(container, verifiably_provides(ITranscriptContainer))
        assert_that(container, has_length(0))
        
        container.add(transcript)
        assert_that(container, has_length(1))
        assert_that(list(container), has_length(1))
        
        assert_that(transcript, has_property('__parent__', is_(video)))

        container.clear()
        assert_that(container, has_length(0))
        assert_that(transcript, has_property('__parent__', is_(none())))
