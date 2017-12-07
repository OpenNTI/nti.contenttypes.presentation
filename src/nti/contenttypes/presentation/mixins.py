#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import interface

from zope.cachedescriptors.property import readproperty

from zope.location.interfaces import IContained

from zope.mimetype.interfaces import IContentTypeAware

from nti.base.interfaces import ICreated

from nti.contenttypes.presentation import NTI

from nti.contenttypes.presentation.common import make_schema
from nti.contenttypes.presentation.common import generate_ntiid

from nti.contenttypes.presentation.interfaces import IPresentationAsset

from nti.dublincore.datastructures import PersistentCreatedModDateTrackingObject

from nti.externalization.representation import WithRepr

from nti.recorder.mixins import RecordableMixin

from nti.schema.field import SchemaConfigured

from nti.schema.interfaces import find_most_derived_interface

logger = __import__('logging').getLogger(__name__)


@WithRepr
@interface.implementer(IContained)
class PersistentMixin(SchemaConfigured,
                      PersistentCreatedModDateTrackingObject):  # order matters

    __name__ = None
    __parent__ = None

    jsonschema = ''

    def __init__(self, *args, **kwargs):
        SchemaConfigured.__init__(self, **kwargs)
        PersistentCreatedModDateTrackingObject.__init__(self, *args, **kwargs)


@total_ordering
@interface.implementer(IPresentationAsset, IContentTypeAware, ICreated)
class PersistentPresentationAsset(PersistentMixin):

    title = None
    byline = None
    description = None

    parameters = {}  # IContentTypeAware

    @readproperty
    def creator(self):  # pylint: disable=method-hidden
        return self.byline

    @classmethod
    def generate_ntiid(cls, nttype, provider=NTI):
        return generate_ntiid(nttype, provider=provider)

    def __lt__(self, other):
        try:
            return (self.mimeType, self.ntiid) < (other.mimeType, other.ntiid)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return (self.mimeType, self.ntiid) > (other.mimeType, other.ntiid)
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def schema(self, user=None):
        schema = find_most_derived_interface(self, IPresentationAsset)
        return make_schema(schema=schema, user=user)


class RecordablePresentationAsset(RecordableMixin,
                                  PersistentPresentationAsset):
    pass
