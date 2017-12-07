#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that

import unittest

from nti.contenttypes.presentation.index import create_assets_library_catalog

from nti.contenttypes.presentation.tests import SharedConfiguringTestLayer


class TestCatalog(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_catalog(self):
        catalog = create_assets_library_catalog()

        catalog.container_index.do_index_doc(1, ('a', 'b'))
        assert_that(list(catalog.get_references(container_ntiids='a')), 
                    is_([1]))

        catalog.unindex_doc(1)
        assert_that(list(catalog.get_references(container_ntiids='b')), 
                    is_([]))
        assert_that(list(catalog.get_references(container_ntiids='a')),
                    is_([]))

        catalog.container_index.do_index_doc(1, ('x', 'y'))
        assert_that(catalog.get_containers(1), has_length(2))

        catalog.update_containers(1, ('z',))
        assert_that(catalog.get_containers(1), has_length(3))

        catalog.update_containers(1, ('z',))
        assert_that(catalog.get_containers(1), has_length(3))

        catalog.remove_containers(1, ('x', 'y'))
        assert_that(catalog.get_containers(1), has_length(1))

        catalog.remove_all_containers(1)
        assert_that(catalog.get_containers(1), has_length(0))
