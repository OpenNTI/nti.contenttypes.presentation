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

from .internalization import course_overview_pre_hook

def create_object_from_external(ext_obj, pre_hook=course_overview_pre_hook):
	factory = find_factory_for(ext_obj)
	assert factory is not None, "Coult not find factory for external object"
	result = factory()
	update_from_external_object(result, ext_obj, pre_hook=pre_hook)
	return result
