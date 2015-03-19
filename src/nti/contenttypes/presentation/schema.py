#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.schema.field import Variant
from nti.schema.field import ValidText
from nti.schema.field import ValidTextLine
from nti.schema.field import ListOrTupleFromObject

def CompoundModeledContentBody(required=False):
	"""
	Returns a :class:`zope.schema.interfaces.IField` representing
	the a compound body 
	"""

	return ListOrTupleFromObject( title="The body of this object",
								  description="An ordered sequence of body parts",
								  value_type=Variant((ValidText(min_length=1, description="Content"),
													  ValidTextLine(min_length=1, description="Content")),
													 title="A body part",
													 __name__='body'),
								  min_length=1,
								  required=required,
								  __name__='body')
