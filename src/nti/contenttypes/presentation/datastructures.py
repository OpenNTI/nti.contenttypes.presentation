#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.contenttypes.presentation.discussion import NTIDiscussionRef

logger = __import__('logging').getLogger(__name__)


def LegacyDiscussionFactory(unused_ext_obj):
    return NTIDiscussionRef
