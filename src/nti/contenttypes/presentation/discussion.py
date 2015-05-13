#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from urllib import unquote
from urlparse import urlparse

from zope import interface

from nti.common.property import readproperty

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_provider_safe
from nti.ntiids.ntiids import make_specific_safe

from nti.schema.schema import EqHash 
from nti.schema.fieldproperty import createDirectFieldProperties

from .interfaces import INTIDiscussionRef

from ._base import PersistentPresentationAsset

from . import DISCUSSION_REF
from . import NTI_COURSE_BUNDLE
		
@interface.implementer(INTIDiscussionRef)
@EqHash('ntiid')
class NTIDiscussionRef(PersistentPresentationAsset):
	createDirectFieldProperties(INTIDiscussionRef)

	__external_class_name__ = u"DiscussionRef"
	mime_type = mimeType = u'application/vnd.nextthought.discussionref'

	@readproperty
	def id(self):
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
		nttype = DISCUSSION_REF + nttype[nttype.index(':'):]
	else:
		nttype = DISCUSSION_REF
	ntiid = make_ntiid(nttype=nttype, base=ntiid)
	return ntiid

def make_discussionref_ntiid_from_bundle_id(iden):
	cmpns = urlparse(iden)
	path = make_specific_safe(cmpns.path)
	netloc = make_provider_safe(unquote(cmpns.netloc))
	ntiid = make_ntiid(provider=netloc, nttype=DISCUSSION_REF, specific=path)
	return ntiid
