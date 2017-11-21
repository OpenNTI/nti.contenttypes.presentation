#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
import importlib
from collections import Mapping

from nti.contenttypes.presentation import AUDIO_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_MIME_TYPES
from nti.contenttypes.presentation import TIMELINE_MIME_TYPES
from nti.contenttypes.presentation import AUDIO_REF_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_REF_MIME_TYPES
from nti.contenttypes.presentation import AUDIO_ROLL_MIME_TYPES
from nti.contenttypes.presentation import SURVEY_REF_MIME_TYPES
from nti.contenttypes.presentation import VIDEO_ROLL_MIME_TYPES
from nti.contenttypes.presentation import QUESTION_REF_MIME_TYPES
from nti.contenttypes.presentation import TIMELINE_REF_MIME_TYPES
from nti.contenttypes.presentation import ASSIGNMENT_REF_MIME_TYPES
from nti.contenttypes.presentation import DISCUSSION_REF_MIME_TYPES
from nti.contenttypes.presentation import SLIDE_DECK_REF_MIME_TYPES
from nti.contenttypes.presentation import LESSON_OVERVIEW_MIME_TYPES
from nti.contenttypes.presentation import QUESTIONSET_REF_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_MIME_TYPES
from nti.contenttypes.presentation import COURSE_OVERVIEW_GROUP_MIME_TYPES

from nti.contenttypes.presentation.internalization import internalization_pollref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntiaudio_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntivideo_pre_hook
from nti.contenttypes.presentation.internalization import internalization_mediaroll_pre_hook
from nti.contenttypes.presentation.internalization import internalization_surveyref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntiaudioref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntivideoref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntitimeline_pre_hook
from nti.contenttypes.presentation.internalization import internalization_questionref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_assignmentref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_discussionref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_questionsetref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_relatedworkref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntitimelineref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntislidedeckref_pre_hook
from nti.contenttypes.presentation.internalization import internalization_ntilessonoverview_pre_hook
from nti.contenttypes.presentation.internalization import internalization_nticourseoverviewgroup_pre_hook

from nti.externalization.interfaces import StandardExternalFields

from nti.externalization.internalization import pre_hook
from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

MIMETYPE = StandardExternalFields.MIMETYPE

logger = __import__('logging').getLogger(__name__)


def prepare_json_text(s):
    result = s.decode('utf-8') if isinstance(s, bytes) else s
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
    update_from_external_object(result, ext_obj,
                                notify=notify, pre_hook=pre_hook)
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
                                         notify=notify,
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
                                         notify=notify,
                                         pre_hook=internalization_assignmentref_pre_hook,
                                         _exec=_exec)
    return result


def create_surveyref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_surveyref_pre_hook,
                                         _exec=_exec)
    return result


def create_pollref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_pollref_pre_hook,
                                         _exec=_exec)
    return result


def create_discussionref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_discussionref_pre_hook,
                                         _exec=_exec)
    return result


def create_ntislidedeckref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_ntislidedeckref_pre_hook,
                                         _exec=_exec)
    return result


def create_relatedworkref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_relatedworkref_pre_hook,
                                         _exec=_exec)
    return result


def create_ntitimeline_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_ntitimeline_pre_hook,
                                         _exec=_exec)
    return result


def create_ntitimelineref_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_ntitimelineref_pre_hook,
                                         _exec=_exec)
    return result


def create_mediaroll_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_mediaroll_pre_hook,
                                         _exec=_exec)
    return result
create_videoroll_from_external = create_mediaroll_from_external  # legacy
create_ntiaudioroll_from_external = create_mediaroll_from_external


def create_nticourseoverviewgroup_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_nticourseoverviewgroup_pre_hook,
                                         _exec=_exec)
    return result


def create_ntilessonoverview_from_external(ext_obj, notify=True, _exec=True):
    result = create_object_from_external(ext_obj,
                                         notify=notify,
                                         pre_hook=internalization_ntilessonoverview_pre_hook,
                                         _exec=_exec)
    return result


def is_media_mimeType(mimeType):
    return bool(mimeType in VIDEO_MIME_TYPES or mimeType in AUDIO_MIME_TYPES)


def is_timeline_mimeType(mimeType):
    return bool(mimeType in TIMELINE_MIME_TYPES)

                
def mime_types():
    for data in (AUDIO_MIME_TYPES,
                 VIDEO_MIME_TYPES,
                 TIMELINE_MIME_TYPES,
                 AUDIO_REF_MIME_TYPES,
                 VIDEO_REF_MIME_TYPES,
                 AUDIO_ROLL_MIME_TYPES,
                 SURVEY_REF_MIME_TYPES,
                 VIDEO_ROLL_MIME_TYPES,
                 QUESTION_REF_MIME_TYPES,
                 TIMELINE_REF_MIME_TYPES,
                 ASSIGNMENT_REF_MIME_TYPES,
                 DISCUSSION_REF_MIME_TYPES,
                 SLIDE_DECK_REF_MIME_TYPES,
                 LESSON_OVERVIEW_MIME_TYPES,
                 QUESTIONSET_REF_MIME_TYPES,
                 RELATED_WORK_REF_MIME_TYPES,
                 COURSE_OVERVIEW_GROUP_MIME_TYPES):
        yield data


_creators_map = None
def get_creators_map():
    global _creators_map
    if _creators_map is None:
        _creators_map = dict()
        module = sys.modules['nti.contenttypes.presentation.utils']
        for data in mime_types():
            for mimeType in data:
                s = mimeType[mimeType.rindex('.') + 1:]
                func = 'create_%s_from_external' % s
                if func in module.__dict__:
                    func = module.__dict__[func]
                    break
            if func is None:
                func = create_object_from_external
            for mime_type in data:
                _creators_map[mime_type] = func
    return _creators_map


def create_from_external(ext_obj, notify=True, _exec=True):
    mimeType = ext_obj.get('mimeType') or ext_obj.get(MIMETYPE)
    creator = get_creators_map().get(mimeType)
    if creator is None:
        creator = create_object_from_external
    return creator(ext_obj, notify=notify, _exec=_exec)


_pre_hooks_map = None
def get_pre_hooks_map():
    global _pre_hooks_map
    if _pre_hooks_map is None:
        _pre_hooks_map = dict()
        module = importlib.import_module('nti.contenttypes.presentation.internalization')
        for data in mime_types():
            for mimeType in data:
                s = mimeType[mimeType.rindex('.') + 1:]
                func = 'internalization_%s_pre_hook' % s
                if func in module.__dict__:
                    func = module.__dict__[func]
                    break
            if func is None:
                func = pre_hook
            for mime_type in data:
                _pre_hooks_map[mime_type] = func
    return _pre_hooks_map


def get_external_pre_hook(ext_obj):
    if isinstance(ext_obj, Mapping):
        mimeType = ext_obj.get('mimeType') or ext_obj.get(MIMETYPE)
    else:
        mimeType = str(ext_obj)
    result = get_pre_hooks_map().get(mimeType)
    if result is None:
        result = pre_hook
    return result
