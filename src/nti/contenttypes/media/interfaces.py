#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

class INTIMedia(interface.Interface):
	pass

class INTIAudio(INTIMedia):
	pass

class INTIVideo(INTIMedia):
	pass