#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import six
import zlib
import base64
from collections import Mapping

from zope import component
from zope import interface

from nti.base.interfaces import IFile

from nti.contenttypes.presentation import PUBLICATION_CONSTRAINTS as PC

from nti.contenttypes.presentation.interfaces import IPointer
from nti.contenttypes.presentation.interfaces import INTIMediaRoll
from nti.contenttypes.presentation.interfaces import IConcreteAsset
from nti.contenttypes.presentation.interfaces import INTITranscript
from nti.contenttypes.presentation.interfaces import INTIAudioSource
from nti.contenttypes.presentation.interfaces import INTIVideoSource
from nti.contenttypes.presentation.interfaces import IUserCreatedAsset
from nti.contenttypes.presentation.interfaces import INTILessonOverview
from nti.contenttypes.presentation.interfaces import INTICourseOverviewGroup
from nti.contenttypes.presentation.interfaces import ILessonPublicationConstraints

from nti.contenttypes.presentation.lesson import constraints_for_lesson

from nti.externalization.autopackage import AutoPackageSearchingScopedInterfaceObjectIO

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.externalization import to_external_object

from nti.externalization.interfaces import IInternalObjectIO
from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import StandardInternalFields
from nti.externalization.interfaces import IInternalObjectExternalizer

from nti.mimetype.externalization import decorateMimeType

from nti.recorder.interfaces import IRecordable
from nti.recorder.interfaces import IRecordableContainer

from nti.publishing.interfaces import IPublishable

OID = StandardExternalFields.OID
CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
ITEMS = StandardExternalFields.ITEMS
MIMETYPE = StandardExternalFields.MIMETYPE
CREATED_TIME = StandardExternalFields.CREATED_TIME
LAST_MODIFIED = StandardExternalFields.LAST_MODIFIED

INTERNAL_NTIID = StandardInternalFields.NTIID


@interface.implementer(IInternalObjectIO)
@component.adapter(INTICourseOverviewGroup)
class _NTICourseOverviewGroupInternalObjectIO(AutoPackageSearchingScopedInterfaceObjectIO):

    _excluded = {ITEMS}
    _excluded_out_ivars_ = _excluded | AutoPackageSearchingScopedInterfaceObjectIO._excluded_out_ivars_

    @classmethod
    def _ap_enumerate_externalizable_root_interfaces(cls, pa_interfaces):
        return (pa_interfaces.INTICourseOverviewGroup,)

    @classmethod
    def _ap_enumerate_module_names(cls):
        return ('group',)

    def toExternalObject(self, *args, **kwargs):
        result = super(_NTICourseOverviewGroupInternalObjectIO, self).toExternalObject(*args, **kwargs)
        result[ITEMS] = [
            to_external_object(x, *args, **kwargs) for x in self._ext_self
        ]
        return result
_NTICourseOverviewGroupInternalObjectIO.__class_init__()


@component.adapter(INTILessonOverview)
@interface.implementer(IInternalObjectIO)
class _NTILessonOverviewInternalObjectIO(AutoPackageSearchingScopedInterfaceObjectIO):

    @classmethod
    def _ap_enumerate_externalizable_root_interfaces(cls, pa_interfaces):
        return (pa_interfaces.INTILessonOverview,)

    @classmethod
    def _ap_enumerate_module_names(cls):
        return ('lesson',)
_NTILessonOverviewInternalObjectIO.__class_init__()


@component.adapter(INTILessonOverview)
@interface.implementer(IInternalObjectExternalizer)
class _LessonOverviewExporter(object):

    def __init__(self, obj):
        self.lesson = obj

    def _decorate_object(self, obj, result):
        decorateMimeType(obj, result)
        if IRecordable.providedBy(obj):
            result['isLocked'] = obj.isLocked()
        if IRecordableContainer.providedBy(obj):
            result['isChildOrderLocked'] = obj.isChildOrderLocked()
        if IPublishable.providedBy(obj):
            result['isPublished'] = obj.isPublished()

    def _decorate_callback(self, obj, result):
        if isinstance(result, Mapping) and MIMETYPE not in result:
            self._decorate_object(obj, result)

    def _process_media_roll(self, asset, roll_items_ext, ext_params):
        for roll_idx, media_ref in enumerate(asset):
            # For user created, make sure we export the media payload
            # Otherwise, export the ref.
            media = IConcreteAsset(media_ref, media_ref)
            if IUserCreatedAsset.providedBy(media):
                media_ext = to_external_object(media, **ext_params)
                roll_items_ext[roll_idx] = media_ext

    def _process_group(self, group, result, ext_params):
        """
        Externalize concrete assets since they are turned into refs on
        import/sync.
        """
        items = result.get(ITEMS) or ()
        for idx, asset in enumerate(group):
            if IPointer.providedBy(asset):
                source = IConcreteAsset(asset, asset)
                ext_obj = to_external_object(source, **ext_params)
                items[idx] = ext_obj
            elif INTIMediaRoll.providedBy(asset):
                roll_items_ext = items[idx].get(ITEMS) or ()
                self._process_media_roll(asset, roll_items_ext, ext_params)

    def toExternalObject(self, *args, **kwargs):
        mod_args = dict(**kwargs)
        mod_args['name'] = ''  # default
        mod_args['decorate'] = False  # no decoration
        mod_args['decorate_callback'] = self._decorate_callback
        result = to_external_object(self.lesson, *args, **mod_args)
        # make sure we have items
        if ITEMS in result and result[ITEMS] is None:
            result[ITEMS] = []
        constraints = constraints_for_lesson(self.lesson, False)
        if constraints:
            result[PC] = to_external_object(constraints, *args, **mod_args)

        # process groups
        mod_args['name'] = 'exporter'  # there may be registered adapters
        for group, ext_obj in zip(self.lesson, result.get(ITEMS) or ()):
            self._process_group(group, ext_obj, mod_args)
        return result


@component.adapter(ILessonPublicationConstraints)
@interface.implementer(IInternalObjectExternalizer)
class _LessonPublicationConstraintsExternalizer(object):

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, *args, **kwargs):
        result = InterfaceObjectIO(
                    self.context,
                    ILessonPublicationConstraints).toExternalObject(*args, **kwargs)
        items = result[ITEMS] = []
        for constraint in self.context.Items or ():
            ext_obj = to_external_object(constraint, *args, **kwargs)
            items.append(ext_obj)
        return result


@component.adapter(INTITranscript)
@interface.implementer(IInternalObjectExternalizer)
class _NTITranscriptExternalizer(InterfaceObjectIO):

    _excluded_out_ivars_ = getattr(InterfaceObjectIO, '_excluded_out_ivars_').union({'src', 'srcjsonp'})

    _ext_iface_upper_bound = INTITranscript

    def toExternalObject(self, **kwargs):
        context = self._ext_replacement()
        result = super(_NTITranscriptExternalizer, self).toExternalObject(**kwargs)
        for name in ('src', 'srcjsonp'):
            if name in result:
                continue
            value = getattr(context, name, None)
            if isinstance(value, six.string_types) or value is None:
                result[name] = value
        return result


@interface.implementer(IInternalObjectExternalizer)
class _NTIMediaSourceExporter(object):

    provided = None

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, *args, **kwargs):
        exporter = InterfaceObjectIO(self.context, self.provided)
        result = exporter.toExternalObject(*args, **kwargs)
        for name in (NTIID, INTERNAL_NTIID, OID):
            result.pop(name, None)
        return result


@component.adapter(INTIAudioSource)
@interface.implementer(IInternalObjectExternalizer)
class _NTIAudioSourceExporter(_NTIMediaSourceExporter):
    provided = INTIAudioSource


@component.adapter(INTIVideoSource)
@interface.implementer(IInternalObjectExternalizer)
class _NTIVideoSourceExporter(_NTIMediaSourceExporter):
    provided = INTIVideoSource


@component.adapter(INTITranscript)
@interface.implementer(IInternalObjectExternalizer)
class _NTITranscriptExporter(object):

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, *args, **kwargs):
        exporter = InterfaceObjectIO(self.context, INTITranscript)
        exporter._excluded_out_ivars_ = {'src'} | exporter._excluded_out_ivars_
        result = exporter.toExternalObject(*args, **kwargs)
        source = self.context.src
        if IFile.providedBy(source):
            data = base64.b64encode(zlib.compress(source.data or b''))
            result['contents'] = data
            result['contentType'] = source.contentType
            result['filename'] = getattr(source, 'filename', None)
        else:
            result['src'] = source
        for name in (NTIID, INTERNAL_NTIID):
            result.pop(name, None)
        return result
