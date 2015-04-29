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

from nti.ntiids.ntiids import get_type
from nti.ntiids.ntiids import make_ntiid
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

	def isCourseBundle(self):
		ntiid = self.ntiid
		cmpns = urlparse(ntiid) if ntiid else None
		result = cmpns.scheme == NTI_COURSE_BUNDLE if cmpns is not None else False
		return result
	is_nti_course_bundle = isCourseBundle

def make_placeholder_ntiid(title=''):
	splits = str(uuid.uuid4()).split('-')
	prefix = '_'.join(splits if not title else splits[0:2])
	prefix = "%s_%s" % (prefix, make_specific_safe(title or u''))
	specific = make_specific_safe(prefix)
	ntiid = make_ntiid(provider='NTI', nttype=DISCUSSION_REF, specific=specific)
	return ntiid
	
def make_discussionref_ntiid(ntiid):
	nttype = get_type(ntiid)
	if nttype and ':' in nttype:
		nttype = DISCUSSION_REF + nttype[nttype.index(':'):]
	else:
		nttype = DISCUSSION_REF
	ntiid = make_ntiid(nttype=nttype, base=ntiid)
	return ntiid
