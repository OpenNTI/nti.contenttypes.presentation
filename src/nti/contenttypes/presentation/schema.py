#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.schema.field import ValidTextLine

logger = __import__('logging').getLogger(__name__)


class VisibilityField(ValidTextLine):

    def __init__(self, *args, **kwargs):
        kwargs.pop('default', None)  # don't validate on creation
        super(VisibilityField, self).__init__(*args, **kwargs)

    @property
    def _options(self):
        # XXX: avoid circular imports
        from nti.contenttypes.presentation.common import get_visibility_options
        return get_visibility_options()

    def _validate(self, value):
        super(VisibilityField, self)._validate(value)
        if value and value not in self._options:
            logger.debug("Unsupported visibility value %s", value)
