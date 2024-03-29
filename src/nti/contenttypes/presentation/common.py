#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import uuid
from datetime import datetime

from zope import component
from zope import interface

from nti.coremetadata.interfaces import SYSTEM_USER_NAME

from nti.contenttypes.presentation import NTI

from nti.contenttypes.presentation.interfaces import CREDIT
from nti.contenttypes.presentation.interfaces import EVERYONE

from nti.contenttypes.presentation.interfaces import IVisibilityOptionsProvider
from nti.contenttypes.presentation.interfaces import IPresentationAssetJsonSchemaMaker

from nti.coremetadata.utils import make_schema as core_schema_maker

from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

logger = __import__('logging').getLogger(__name__)


def generate_ntiid(nttype, provider=NTI, now=None):
    now = datetime.utcnow() if now is None else now
    dstr = now.strftime("%Y%m%d%H%M%S %f")
    rand = str(uuid.uuid4().time_low)
    specific = make_specific_safe(u"%s_%s_%s" % (SYSTEM_USER_NAME, dstr, rand))
    result = make_ntiid(provider=provider,
                        nttype=nttype,
                        specific=specific)
    return result


def make_schema(schema, user=None):
    result = core_schema_maker(schema,
                               user=user,
                               maker=IPresentationAssetJsonSchemaMaker)
    return result


@interface.implementer(IVisibilityOptionsProvider)
class DefaultVisibilityOptionProvider(object):

    __slots__ = ()

    def __init__(self, *args):
        pass

    def iter_options(self):
        return (EVERYONE, CREDIT)


def get_visibility_options():
    result = set()
    for _, provider in list(component.getUtilitiesFor(IVisibilityOptionsProvider)):
        result.update(provider.iter_options())
    return tuple(result)
