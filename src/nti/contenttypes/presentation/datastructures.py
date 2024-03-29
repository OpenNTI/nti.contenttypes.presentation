#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import copy
from collections import Mapping
from collections import MutableSequence

from nti.contenttypes.presentation import TIMELINE
from nti.contenttypes.presentation import RELATED_WORK
from nti.contenttypes.presentation import JSON_TIMELINE
from nti.contenttypes.presentation import RELATED_WORK_REF
from nti.contenttypes.presentation import TIMELINE_MIME_TYPES
from nti.contenttypes.presentation import SLIDE_DECK_MIME_TYPES
from nti.contenttypes.presentation import TIMELINE_REF_MIME_TYPES
from nti.contenttypes.presentation import ALL_MEDIA_ROLL_MIME_TYPES
from nti.contenttypes.presentation import SLIDE_DECK_REF_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_MIME_TYPES
from nti.contenttypes.presentation import RELATED_WORK_REF_POINTER_MIME_TYPES

from nti.contenttypes.presentation.discussion import is_nti_course_bundle

from nti.contenttypes.presentation.group import NTICourseOverViewGroup

from nti.contenttypes.presentation.lesson import NTILessonOverView

from nti.externalization.interfaces import StandardExternalFields

from nti.ntiids.ntiids import is_ntiid_of_type
from nti.ntiids.ntiids import is_ntiid_of_types

ID = StandardExternalFields.ID
ITEMS = StandardExternalFields.ITEMS
NTIID = StandardExternalFields.NTIID
MIMETYPE = StandardExternalFields.MIMETYPE

LEGACY_MIMETYPE_MAPPING = {
    # discussions
    "application/vnd.nextthought.discussion": "application/vnd.nextthought.discussionref",
    # assessments
    "application/vnd.nextthought.assessment.assignment": "application/vnd.nextthought.assignmentref",
    "application/vnd.nextthought.naquestionset": "application/vnd.nextthought.questionsetref",
    "application/vnd.nextthought.naquestion": "application/vnd.nextthought.questionref",
    "application/vnd.nextthought.nasurvey": "application/vnd.nextthought.surveyref",
    "application/vnd.nextthought.napoll": "application/vnd.nextthought.pollref",
    # media
    "application/vnd.nextthought.ntivideoroll": "application/vnd.nextthought.videoroll",
    "application/vnd.nextthought.ntiaudio": "application/vnd.nextthought.ntiaudioref",
    "application/vnd.nextthought.ntivideo": "application/vnd.nextthought.ntivideoref",
}

logger = __import__('logging').getLogger(__name__)


def legacy_ntimedia_transform(ext_obj):
    if isinstance(ext_obj, Mapping) and 'mimeType' in ext_obj:
        ext_obj[MIMETYPE] = ext_obj.pop('mimeType')
    return ext_obj
legacy_ntiaudio_transform = legacy_ntimedia_transform
legacy_ntivideo_transform = legacy_ntimedia_transform


def legacy_ntislidedeckref_transform(ext_obj):
    mimeType = ext_obj.get(MIMETYPE) if isinstance(ext_obj, Mapping) else None
    if mimeType in SLIDE_DECK_MIME_TYPES:
        ext_obj[MIMETYPE] = SLIDE_DECK_REF_MIME_TYPES[0]
    return ext_obj


def is_timeline(x):
    result = False
    mimeType = x.get(MIMETYPE) if isinstance(x, Mapping) else None
    if not mimeType:
        if isinstance(x, Mapping):
            ntiid = x.get('ntiid') or x.get(NTIID)
        else:
            ntiid = None
        if ntiid and (JSON_TIMELINE in ntiid or is_ntiid_of_type(ntiid, TIMELINE)):
            result = True
    elif mimeType in TIMELINE_MIME_TYPES:
        result = True
    return result


def legacy_ntitimeline_transform(ext_obj):
    if is_timeline(ext_obj):
        ext_obj[MIMETYPE] = TIMELINE_MIME_TYPES[0]
    return ext_obj


def legacy_ntitimelineref_transform(ext_obj):
    if is_timeline(ext_obj):
        ext_obj[MIMETYPE] = TIMELINE_REF_MIME_TYPES[0]
    return ext_obj


def is_relatedwork_ref(ext_obj):
    result = False
    mimeType = ext_obj.get(MIMETYPE) if isinstance(ext_obj, Mapping) else None
    if not mimeType:
        if isinstance(ext_obj, Mapping):
            ntiid = ext_obj.get('ntiid') or ext_obj.get(NTIID)
        else:
            ntiid = None
        # check ntiid
        if       ntiid \
            and (   '.relatedworkref.' in ntiid
                 or is_ntiid_of_types(ntiid, (RELATED_WORK, RELATED_WORK_REF))):
            result = True
    elif mimeType in RELATED_WORK_REF_MIME_TYPES:
        result = True
    return result


def legacy_relatedworkref_transform(ext_obj):
    if is_relatedwork_ref(ext_obj):
        ext_obj[MIMETYPE] = RELATED_WORK_REF_MIME_TYPES[0]
    return ext_obj


def legacy_relatedworkrefpointer_transform(ext_obj):
    if is_relatedwork_ref(ext_obj):
        ext_obj[MIMETYPE] = RELATED_WORK_REF_POINTER_MIME_TYPES[0]
    return ext_obj


def legacy_mediaroll_transform(ext_obj):
    if isinstance(ext_obj, MutableSequence):
        for item in ext_obj:
            # pylint: disable=too-many-function-args
            legacy_transform(None, item)
    return ext_obj


def legacy_transform(ext_obj):
    if isinstance(ext_obj, Mapping):
        mimeType = ext_obj.get(MIMETYPE) or ext_obj.get('mimeType')
        ext_obj[MIMETYPE] = LEGACY_MIMETYPE_MAPPING.get(mimeType, mimeType)
        ext_obj.pop('mimeType', None)
    return ext_obj


def legacy_nticourseoverviewgroup_transform(ext_obj):
    items = ext_obj.get(ITEMS)
    if isinstance(items, MutableSequence):
        idx = 0
        while idx < len(items):
            item = items[idx]
            # Swizzle out our concrete mime types for refs.
            # don't include timelineref or relatedworkrefs pointers
            # as we need the definitions during import
            legacy_transform(item)
            legacy_ntislidedeckref_transform(item)

            # do checks
            mimeType = None
            if isinstance(item, Mapping):
                mimeType = item.get(MIMETYPE)

            # handle discussions (mimeType has been transformed)
            if mimeType == "application/vnd.nextthought.discussionref":
                iden = item.get('id') or item.get(ID)
                s = item.get(NTIID) or item.get('ntiid')
                ntiids = s.split(' ') if s else ()
                if len(ntiids) > 1:
                    for counter, ntiid in enumerate(ntiids):
                        if counter > 0:
                            idx += 1
                            item = copy.deepcopy(item)
                            items.insert(idx, item)
                        item[NTIID] = ntiid
                        legacy_transform(item)
                # not yet ready
                elif not ntiids and not is_nti_course_bundle(iden):
                    del items[idx]
                    continue
                else:
                    legacy_transform(item)

            # handle media rolls
            if mimeType in ALL_MEDIA_ROLL_MIME_TYPES:
                legacy_mediaroll_transform(item.get(ITEMS))

            # check next
            idx += 1
    return ext_obj


def legacy_ntilessonoverview_transform(ext_obj):
    items = ext_obj.get(ITEMS)
    if isinstance(items, MutableSequence):
        for item in items:
            legacy_nticourseoverviewgroup_transform(item)
    return ext_obj


def CourseOverViewGroupFactory(unused_ext_obj):
    # legacy_nticourseoverviewgroup_transform(ext_obj)
    return NTICourseOverViewGroup


def LessonOverViewFactory(unused_ext_obj):
    # legacy_ntilessonoverview_transform(ext_obj)
    return NTILessonOverView
