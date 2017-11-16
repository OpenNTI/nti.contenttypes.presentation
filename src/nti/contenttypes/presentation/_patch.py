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
    import sys
    import inspect
    import importlib

    from nti.contenttypes.presentation.interfaces import IGroupOverViewable
    module = sys.modules[IGroupOverViewable.__module__]

    # main package name
    package = '.'.join(module.__name__.split('.')[:-1])

    # set mimetypes on interfaces
    for name in os.listdir(os.path.dirname(__file__)):
        # ignore modules we may have trouble importing
        if name in ('__init__.py',
                    '_patch.py',
                    'jsonschema.py',
                    'externalization.py',
                    'internalization.py') \
                or name[-3:] != '.py':
            continue

        try:
            module = package + '.' + name[:-3]
            module = importlib.import_module(module)
        except ImportError:
            continue

        for _, item in inspect.getmembers(module):
            try:
                mimeType = getattr(item, 'mimeType', None) \
                        or getattr(item, 'mime_type')
                # first interface is the externalizable object
                interfaces = tuple(item.__implemented__.interfaces())
                interfaces[0].setTaggedValue('_ext_mime_type', mimeType)
            except (AttributeError, TypeError):
                pass


_patch()
del _patch


def patch():
    pass
