#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from six.moves import urllib_parse
from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.contenttypes.presentation import NTI_COURSE_BUNDLE
from nti.contenttypes.presentation import NTI_DISCUSSION_REF

from nti.contenttypes.presentation.interfaces import INTIDiscussionRef

from nti.contenttypes.presentation.mixins import RecordablePresentationAsset

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid

from nti.schema.fieldproperty import createDirectFieldProperties

logger = __import__('logging').getLogger(__name__)


@total_ordering
@interface.implementer(INTIDiscussionRef)
class NTIDiscussionRef(RecordablePresentationAsset):
    createDirectFieldProperties(INTIDiscussionRef)

    __external_class_name__ = "DiscussionRef"
    mime_type = mimeType = 'application/vnd.nextthought.discussionref'

    @readproperty
    def ntiid(self):  # pylint: disable=method-hidden
        self.ntiid = self.generate_ntiid(NTI_DISCUSSION_REF)
        return self.ntiid

    @readproperty
    def id(self):
        return self.ntiid

    @readproperty
    def target(self):
        return self.id or self.ntiid

    def isCourseBundle(self):
        return is_nti_course_bundle(self.id or self.ntiid)
    is_course_bundle = is_nti_course_bundle = isCourseBundle

    def __lt__(self, other):
        try:
            return (self.mimeType, self.title) < (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.title) > (other.mimeType, other.title)
        except AttributeError:  # pragma: no cover
            return NotImplemented


def is_nti_course_bundle(iden):
    cmpns = urllib_parse.urlparse(iden) if iden else None
    result = cmpns.scheme == NTI_COURSE_BUNDLE if cmpns is not None else False
    return result


def make_discussionref_ntiid(ntiid):
    nttype = get_type(ntiid)
    if nttype and ':' in nttype:
        nttype = NTI_DISCUSSION_REF + nttype[nttype.index(':'):]
    else:
        nttype = NTI_DISCUSSION_REF
    return make_ntiid(nttype=nttype, base=ntiid)
