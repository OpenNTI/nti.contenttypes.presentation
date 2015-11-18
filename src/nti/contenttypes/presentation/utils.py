#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from collections import Mapping

from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import pre_hook
from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from .internalization import internalization_pollref_pre_hook
from .internalization import internalization_ntiaudio_pre_hook
from .internalization import internalization_ntivideo_pre_hook
from .internalization import internalization_surveyref_pre_hook
from .internalization import internalization_ntiaudioref_pre_hook
from .internalization import internalization_ntivideoref_pre_hook
from .internalization import internalization_ntitimeline_pre_hook
from .internalization import internalization_questionref_pre_hook
from .internalization import internalization_assignmentref_pre_hook
from .internalization import internalization_discussionref_pre_hook
from .internalization import internalization_courseoverview_pre_hook
from .internalization import internalization_lessonoverview_pre_hook
from .internalization import internalization_questionsetref_pre_hook
from .internalization import internalization_relatedworkref_pre_hook

from . import AUDIO_MIMETYES
from . import VIDEO_MIMETYES
from . import POLL_REF_MIMETYES
from . import TIMELINE_MIMETYES
from . import AUDIO_REF_MIMETYES
from . import VIDEO_REF_MIMETYES
from . import SURVEY_REF_MIMETYES
from . import QUESTION_REF_MIMETYES
from . import ASSIGNMENT_REF_MIMETYES
from . import DISCUSSION_REF_MIMETYES
from . import LESSON_OVERVIEW_MIMETYES
from . import QUESTIONSET_REF_MIMETYES
from . import RELATED_WORK_REF_MIMETYES
from . import COURSE_OVERVIEW_GROUP_MIMETYES

MIMETYPE = StandardExternalFields.MIMETYPE

def prepare_json_text(s):
	result = unicode(s, 'utf-8') if isinstance(s, bytes) else s
	return result

def create_object_from_external(ext_obj, pre_hook=pre_hook, notify=True, _exec=True):
	__traceback_info__ = ext_obj
	# CS: We want to call prehook in case we can to update a single dict.
	pre_hook(None, ext_obj)
	# find factory
	factory = find_factory_for(ext_obj)
	if _exec:
		assert factory is not None, "Could not find factory for external object"
	# create and update
	result = factory()
	update_from_external_object(result, ext_obj, notify=notify, pre_hook=pre_hook)
	return result

def create_ntiaudio_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_ntiaudio_pre_hook,
										 _exec=_exec)
	return result

def create_ntivideo_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_ntivideo_pre_hook,
										 _exec=_exec)
	return result

def create_ntivideoref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_ntivideoref_pre_hook,
										 _exec=_exec)
	return result

def create_ntiaudioref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_ntiaudioref_pre_hook,
										 _exec=_exec)
	return result

def create_questionref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_questionref_pre_hook,
										 _exec=_exec)
	return result

def create_questionsetref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_questionsetref_pre_hook,
										 _exec=_exec)
	return result

def create_assignmentref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_assignmentref_pre_hook,
										 _exec=_exec)
	return result

def create_surveyref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_surveyref_pre_hook,
										 _exec=_exec)
	return result

def create_pollref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 pre_hook=internalization_pollref_pre_hook,
										 _exec=_exec)
	return result

def create_discussionref_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_discussionref_pre_hook,
										 _exec=_exec)
	return result

def create_relatedwork_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_relatedworkref_pre_hook,
										 _exec=_exec)
	return result

def create_timelime_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_ntitimeline_pre_hook,
										 _exec=_exec)
	return result

def create_courseoverview_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_courseoverview_pre_hook,
										 _exec=_exec)
	return result

def create_lessonoverview_from_external(ext_obj, notify=True, _exec=True):
	result = create_object_from_external(ext_obj,
										 notify=notify,
										 pre_hook=internalization_lessonoverview_pre_hook,
										 _exec=_exec)
	return result

def create_from_external(ext_obj, notify=True, _exec=True):
	mimeType = ext_obj.get('mimeType') or ext_obj.get(MIMETYPE)
	if mimeType in LESSON_OVERVIEW_MIMETYES:
		result = create_lessonoverview_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in COURSE_OVERVIEW_GROUP_MIMETYES:
		result = create_courseoverview_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in TIMELINE_MIMETYES:
		result = create_timelime_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in RELATED_WORK_REF_MIMETYES:
		result = create_relatedwork_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in DISCUSSION_REF_MIMETYES:
		result = create_discussionref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in POLL_REF_MIMETYES:
		result = create_pollref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in SURVEY_REF_MIMETYES:
		result = create_surveyref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in ASSIGNMENT_REF_MIMETYES:
		result = create_assignmentref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in QUESTIONSET_REF_MIMETYES:
		result = create_questionsetref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in QUESTION_REF_MIMETYES:
		result = create_questionref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in VIDEO_REF_MIMETYES:
		result = create_ntivideoref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in AUDIO_REF_MIMETYES:
		result = create_ntiaudioref_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in VIDEO_MIMETYES:
		result = create_ntivideo_from_external(ext_obj, notify=notify, _exec=_exec)
	elif mimeType in AUDIO_MIMETYES:
		result = create_ntiaudio_from_external(ext_obj, notify=notify, _exec=_exec)
	else:
		result = create_object_from_external(ext_obj, notify=notify, _exec=_exec)
	return result

def get_external_pre_hook(ext_obj):
	if isinstance(ext_obj, Mapping):
		mimeType = ext_obj.get('mimeType') or ext_obj.get(MIMETYPE)
	else:
		mimeType = str(ext_obj)

	if mimeType in LESSON_OVERVIEW_MIMETYES:
		result = internalization_lessonoverview_pre_hook
	elif mimeType in COURSE_OVERVIEW_GROUP_MIMETYES:
		result = internalization_courseoverview_pre_hook
	elif mimeType in TIMELINE_MIMETYES:
		result = internalization_ntitimeline_pre_hook
	elif mimeType in RELATED_WORK_REF_MIMETYES:
		result = internalization_relatedworkref_pre_hook
	elif mimeType in DISCUSSION_REF_MIMETYES:
		result = internalization_discussionref_pre_hook
	elif mimeType in POLL_REF_MIMETYES:
		result = internalization_pollref_pre_hook
	elif mimeType in SURVEY_REF_MIMETYES:
		result = internalization_surveyref_pre_hook
	elif mimeType in ASSIGNMENT_REF_MIMETYES:
		result = internalization_assignmentref_pre_hook
	elif mimeType in QUESTIONSET_REF_MIMETYES:
		result = internalization_questionsetref_pre_hook
	elif mimeType in QUESTION_REF_MIMETYES:
		result = internalization_questionref_pre_hook
	elif mimeType in VIDEO_REF_MIMETYES:
		result = internalization_ntivideoref_pre_hook
	elif mimeType in AUDIO_REF_MIMETYES:
		result = internalization_ntiaudioref_pre_hook
	elif mimeType in VIDEO_MIMETYES:
		result = internalization_ntivideo_pre_hook
	elif mimeType in AUDIO_MIMETYES:
		result = internalization_ntiaudio_pre_hook
	else:
		result = pre_hook
	return result
