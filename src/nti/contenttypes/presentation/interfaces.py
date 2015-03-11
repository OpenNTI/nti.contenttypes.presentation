#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Int
from nti.schema.field import Number
from nti.schema.field import ValidTextLine

class INTISlide(interface.Interface):
	slidevideoid = ValidNTIID(title="Slide video NTIID", required=True)
	slidedeckid = ValidNTIID(title="Slide deck NTIID", required=False)
	slidevideostart = Number(title="Video start", required=False, default=0)
	slidevideoend = Number(title="Video end", required=False, default=0)
	ntiid = ValidNTIID(title="Slide NTIID", required=True)
	slideimage = ValidTextLine(title="Slide image source", required=False)
	slidenumber = Int(title="Slide number", required=True, default=1)
