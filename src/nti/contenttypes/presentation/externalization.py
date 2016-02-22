#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttypes.presentation.interfaces import INTITimeline
from nti.contenttypes.presentation.interfaces import INTIRelatedWorkRef

from nti.externalization.autopackage import AutoPackageSearchingScopedInterfaceObjectIO

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.externalization import toExternalObject

from nti.externalization.interfaces import IInternalObjectIO
from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import IInternalObjectExternalizer

OID = StandardExternalFields.OID
CLASS = StandardExternalFields.CLASS
NTIID = StandardExternalFields.NTIID
ITEMS = StandardExternalFields.ITEMS
MIMETYPE = StandardExternalFields.MIMETYPE
CREATED_TIME = StandardExternalFields.CREATED_TIME
LAST_MODIFIED = StandardExternalFields.LAST_MODIFIED

@interface.implementer(IInternalObjectIO)
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
		result[ITEMS] = [toExternalObject(x) for x in self._ext_self]
		return result
_NTICourseOverviewGroupInternalObjectIO.__class_init__()

@component.adapter(INTIRelatedWorkRef)
@interface.implementer(IInternalObjectExternalizer)
class _NTIRelatedWorkRefExternalizer(object):

	def __init__(self, obj):
		self.obj = obj

	def toExternalObject(self, **kwargs):
		result = InterfaceObjectIO(self.obj, INTIRelatedWorkRef).toExternalObject(**kwargs)
		result['href'] = self.obj.href
		return result

@component.adapter(INTITimeline)
@interface.implementer(IInternalObjectExternalizer)
class _NTITimelineExternalizer(object):

	def __init__(self, obj):
		self.obj = obj

	def toExternalObject(self, **kwargs):
		result = InterfaceObjectIO(self.obj, INTITimeline).toExternalObject(**kwargs)
		result['href'] = self.obj.href
		return result
