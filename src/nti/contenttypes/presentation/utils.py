#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.externalization.internalization import pre_hook
from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from .internalization import internalization_ntiaudio_pre_hook
from .internalization import internalization_ntivideo_pre_hook
from .internalization import internalization_ntiaudioref_pre_hook
from .internalization import internalization_ntivideoref_pre_hook
from .internalization import internalization_assignmentref_pre_hook
from .internalization import internalization_discussionref_pre_hook
from .internalization import internalization_courseoverview_pre_hook
from .internalization import internalization_lessonoverview_pre_hook
from .internalization import internalization_relatedworkref_pre_hook

def create_object_from_external(ext_obj, pre_hook=pre_hook, _exec=True):
	__traceback_info__ = ext_obj
	## CS: We want to call prehook in case we can to update a single dict.
	pre_hook(None, ext_obj)
	## find factory
	factory = find_factory_for(ext_obj)
	if _exec:
		assert factory is not None, "Could not find factory for external object"
	## create and update
	result = factory()
	update_from_external_object(result, ext_obj, pre_hook=pre_hook)
	return result

def create_ntiaudio_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_ntiaudio_pre_hook,
										 _exec=_exec)
	return result

def create_ntivideo_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_ntivideo_pre_hook,
										 _exec=_exec)
	return result

def create_ntivideoref_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_ntivideoref_pre_hook,
										 _exec=_exec)
	return result

def create_ntiaudioref_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_ntiaudioref_pre_hook,
										 _exec=_exec)
	return result

def create_assignmentref_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_assignmentref_pre_hook,
										 _exec=_exec)
	return result

def create_discussionref_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_discussionref_pre_hook,
										 _exec=_exec)
	return result

def create_relatedwork_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_relatedworkref_pre_hook,
										 _exec=_exec)
	return result

def create_courseoverview_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_courseoverview_pre_hook,
										 _exec=_exec)
	return result

def create_lessonoverview_from_external(ext_obj, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_lessonoverview_pre_hook,
										 _exec=_exec)
	return result
