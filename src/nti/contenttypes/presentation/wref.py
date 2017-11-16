#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from functools import total_ordering

from zope import component
from zope import interface

from nti.contenttypes.presentation import IPresentationAsset

from nti.ntiids.ntiids import validate_ntiid_string

from nti.property.property import alias

from nti.schema.eqhash import EqHash

from nti.wref.interfaces import IWeakRef

logger = __import__('logging').getLogger(__name__)


@total_ordering
@EqHash('ntiid')
@interface.implementer(IWeakRef)
@component.adapter(IPresentationAsset)
class PresentationAssetWeakRef(object):

    __slots__ = ('ntiid',)

    _ntiid = alias('ntiid')

    def __init__(self, item):
        self.ntiid = item.ntiid
        validate_ntiid_string(self.ntiid)

    def __call__(self):
        # We're not a caching weak ref
        return component.queryUtility(IPresentationAsset, name=self.ntiid)

    def __lt__(self, other):
        try:
            return self.ntiid < other.ntiid
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.ntiid > other.ntiid
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __getstate__(self):
        return (1, self.ntiid)

    def __setstate__(self, state):
        assert state[0] == 1
        self.ntiid = state[1]


def presentation_asset_wref_to_missing_ntiid(ntiid):
    validate_ntiid_string(ntiid)
    wref = PresentationAssetWeakRef.__new__(PresentationAssetWeakRef)
    wref.ntiid = ntiid
    return wref
