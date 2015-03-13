#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from .internalization import internalization_pre_hook

def create_object_from_external(ext_obj, pre_hook=internalization_pre_hook, _exec=True):
	__traceback_info__ = ext_obj
	## CS: We want to call prehook in case we can to update a single dict.
	pre_hook(None, ext_obj)
	## find factory
	factory = find_factory_for(ext_obj)
	if not _exec:
		assert factory is not None, "Could not find factory for external object"
	## create and update
	result = factory()
	update_from_external_object(result, ext_obj, pre_hook=pre_hook)
	return result
