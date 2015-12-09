#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import uuid
from urlparse import urlparse

from zope import interface

from zope.cachedescriptors.property import readproperty

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

from nti.schema.schema import EqHash
from nti.schema.fieldproperty import createDirectFieldProperties

from ._base import PersistentPresentationAsset

from .interfaces import INTIDiscussionRef

from . import NTI_COURSE_BUNDLE
from . import NTI_DISCUSSION_REF
from . import NTI_COURSE_BUNDLE_REF

@EqHash('ntiid')
@interface.implementer(INTIDiscussionRef)
class NTIDiscussionRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIDiscussionRef)

	__external_class_name__ = u"DiscussionRef"
	mime_type = mimeType = u'application/vnd.nextthought.discussionref'

	@readproperty
	def ntiid(self):
		self.ntiid = self.generate_ntiid(NTI_DISCUSSION_REF)
		return self.ntiid
	
	@readproperty
	def id(self):
		return self.ntiid
	
	@readproperty
	def target(self):
		return self.ntiid

	def isCourseBundle(self):
		return is_nti_course_bundle(self.id or self.ntiid)
	is_nti_course_bundle = isCourseBundle

def is_nti_course_bundle(iden):
	cmpns = urlparse(iden) if iden else None
	result = cmpns.scheme == NTI_COURSE_BUNDLE if cmpns is not None else False
	return result

def make_discussionref_ntiid(ntiid):
	nttype = get_type(ntiid)
	if nttype and ':' in nttype:
		nttype = NTI_DISCUSSION_REF + nttype[nttype.index(':'):]
	else:
		nttype = NTI_DISCUSSION_REF
	ntiid = make_ntiid(nttype=nttype, base=ntiid)
	return ntiid

def make_discussionref_ntiid_from_bundle_id(iden):
	provider = str(uuid.uuid4()).split('-')[0].upper()
	path = make_specific_safe(iden[len(NTI_COURSE_BUNDLE_REF):])
	ntiid = make_ntiid(provider=provider, nttype=NTI_DISCUSSION_REF, specific=path)
	return ntiid
