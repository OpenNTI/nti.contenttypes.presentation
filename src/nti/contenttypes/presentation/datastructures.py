#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.contenttypes.presentation.assessment import NTIPollRef

logger = __import__('logging').getLogger(__name__)


def LegacyPollRefFactory(unused_ext_obj):
    return NTIPollRef
