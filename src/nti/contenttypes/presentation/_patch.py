#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)


def _patch():
    import os
    import inspect
    import importlib

    # main package name
    package = '.'.join(__name__.split('.')[:-1])

    ignore_list = ('__init__.py', '_patch.py', 'jsonschema.py',
                   'datastructures.py', 'externalization.py', 'internalization.py')

    # set mimetypes on interfaces
    for name in os.listdir(os.path.dirname(__file__)):
        # ignore modules we may have trouble importing
        if name in ignore_list or name[-3:] != '.py':
            continue

        module = package + '.' + name[:-3]
        module = importlib.import_module(module)

        for _, item in inspect.getmembers(module):
            mimeType = getattr(item, 'mimeType', None) \
                    or getattr(item, 'mime_type', None)
            if mimeType:
                # first interface is the externalizable object
                interfaces = tuple(item.__implemented__.interfaces())
                interfaces[0].setTaggedValue('_ext_mime_type', mimeType)


_patch()
del _patch


def patch():
    pass
