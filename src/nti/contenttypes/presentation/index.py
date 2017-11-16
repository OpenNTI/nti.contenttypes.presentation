#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
import time

from zope import component

from zope.catalog.interfaces import ICatalog

from zope.intid.interfaces import IIntIds

from zope.location import locate

from zc.catalog.index import SetIndex as ZC_SetIndex

import BTrees

from nti.base._compat import integer_types

from nti.contenttypes.presentation.interfaces import ISiteAdapter
from nti.contenttypes.presentation.interfaces import INTIIDAdapter
from nti.contenttypes.presentation.interfaces import ITargetAdapter
from nti.contenttypes.presentation.interfaces import INamespaceAdapter
from nti.contenttypes.presentation.interfaces import ISlideDeckAdapter
from nti.contenttypes.presentation.interfaces import IContainersAdapter
from nti.contenttypes.presentation.interfaces import IPresentationAsset
from nti.contenttypes.presentation.interfaces import IContainedTypeAdapter

from nti.externalization.proxy import removeAllProxies

from nti.zodb.containers import bit64_int_to_time
from nti.zodb.containers import time_to_64bit_int

from nti.zope_catalog.catalog import Catalog
from nti.zope_catalog.catalog import ResultSet

from nti.zope_catalog.index import AttributeSetIndex
from nti.zope_catalog.index import AttributeValueIndex as ValueIndex

ASSETS_CATALOG_INDEX_NAME = 'nti.dataserver.++etc++presentation-assets.catalog'

#: Asset site catalog
IX_SITE = 'site'

#: Asset type (interface name)
IX_TYPE = 'type'

#: Asset NTIID
IX_NTIID = 'ntiid'

#: Asset target NTIID
IX_TARGET = 'target'

#: Asset mimeType
IX_MIMETYPE = 'mimeType'

#: Asset unique namespace
IX_NAMESPACE = 'namespace'

#: Asset containers
IX_CONTAINERS = 'containers'

#: Asset slide deck videos
IX_SLIDEDECK_VIDEOS = 'slideDeckVideos'

logger = __import__('logging').getLogger(__name__)


def to_iterable(value):
    if isinstance(value, (list, tuple, set)):
        result = value
    else:
        result = (value,) if value is not None else ()
    return tuple(getattr(x, '__name__', x) for x in result)


def get_uid(item, intids=None):
    if not isinstance(item, integer_types):
        item = removeAllProxies(item)
        intids = component.getUtility(IIntIds) if intids is None else intids
        return intids.queryId(item)
    return item


class RetainSetIndex(AttributeSetIndex):
    """
    A set index that retains the old values.
    """

    def to_iterable(self, value=None):
        result = to_iterable(value)
        return result

    def do_index_doc(self, doc_id, value):
        # only index if there is a difference between new and stored values
        value = {v for v in self.to_iterable(value) if v is not None}
        old = self.documents_to_values.get(doc_id) or set()
        if value.difference(old):
            value.update(old)
            # call zc.catalog.index.SetIndex which does the actual indexation
            result = ZC_SetIndex.index_doc(self, doc_id, value)
            return result
    index_containers = do_index_doc

    def index_doc(self, doc_id, value):
        if self.interface is not None:
            value = self.interface(value, None)
            if value is None:
                return None
        value = getattr(value, self.field_name, None)
        if value is not None and self.field_callable:
            # do not eat the exception raised below
            value = value()
        # Do not unindex if value is None in order to
        # retain indexed values
        if value is not None:
            return self.do_index_doc(doc_id, value)

    def remove(self, doc_id, containers):
        old = set(self.documents_to_values.get(doc_id) or ())
        if not old:
            return
        for v in to_iterable(containers):
            old.discard(v)
        if old:
            # call zc.catalog.index.SetIndex which does the actual indexation
            return ZC_SetIndex.index_doc(self, doc_id, old)
        else:
            super(RetainSetIndex, self).unindex_doc(doc_id)


class SiteIndex(ValueIndex):
    default_field_name = 'site'
    default_interface = ISiteAdapter


class TypeIndex(ValueIndex):
    default_field_name = 'type'
    default_interface = IContainedTypeAdapter


class TargetIndex(ValueIndex):
    default_field_name = 'target'
    default_interface = ITargetAdapter


class NamespaceIndex(ValueIndex):
    default_field_name = 'namespace'
    default_interface = INamespaceAdapter


class NTIIDIndex(ValueIndex):
    default_field_name = 'ntiid'
    default_interface = INTIIDAdapter


class ContainersIndex(RetainSetIndex):
    default_field_name = 'containers'
    interface = default_interface = IContainersAdapter


class SlideDeckVideosIndex(AttributeSetIndex):
    default_field_name = 'videos'
    interface = default_interface = ISlideDeckAdapter


class MimeTypeIndex(ValueIndex):
    default_field_name = 'mimeType'
    default_interface = IPresentationAsset


class AssetsLibraryCatalog(Catalog):

    family = BTrees.family64

    def __init__(self, family=None):
        super(AssetsLibraryCatalog, self).__init__(family=family)
        self.last_modified = self.family.OI.BTree()

    def clear(self):
        super(AssetsLibraryCatalog, self).clear()
        for index in self.values():
            index.clear()
        self.last_modified.clear()
    reset = clear

    # last modified

    def get_last_modified(self, namespace):
        try:
            return bit64_int_to_time(self.last_modified[namespace])
        except KeyError:
            return 0
    getLastModified = get_last_modified

    def set_last_modified(self, namespace, t=None):
        assert isinstance(namespace, six.string_types)
        t = time.time() if t is None else t
        self.last_modified[namespace] = time_to_64bit_int(t)
    setLastModified = set_last_modified

    def remove_last_modified(self, namespace):
        try:
            del self.last_modified[namespace]
        except KeyError:
            pass
    removeLastModified = remove_last_modified

    def index_doc(self, docid, texts):
        Catalog.index_doc(self, docid, texts)

    def unindex_doc(self, docid):
        Catalog.unindex_doc(self, docid)

    # containers

    @property
    def container_index(self):
        return self[IX_CONTAINERS]

    def get_containers(self, item, intids=None):
        doc_id = get_uid(item, intids)
        if doc_id is not None:
            result = self.container_index.documents_to_values.get(doc_id)
            return set(result or ())
        return set()

    def update_containers(self, item, containers=(), intids=None):
        doc_id = get_uid(item, intids)
        if doc_id is not None and containers:
            containers = to_iterable(containers)
            result = self.container_index.do_index_doc(doc_id, containers)
            return result
        return None

    def remove_containers(self, item, containers, intids=None):
        doc_id = get_uid(item, intids)
        if doc_id is not None:
            self.container_index.remove(doc_id, containers)
            return True
        return False

    def remove_all_containers(self, item, intids=None):
        doc_id = get_uid(item, intids)
        if doc_id is not None:
            self.container_index.unindex_doc(doc_id)
            return True
        return False

    # namespaces

    def namespace_index(self):
        return self[IX_NAMESPACE]

    def get_namespace(self, item, intids=None):
        doc_id = get_uid(item, intids)
        if doc_id is not None:
            return self.namespace_index.documents_to_values.get(doc_id)
        return None

    # search

    def get_references(self,
                       ntiid=None,
                       sites=None,
                       target=None,
                       mimetype=None,
                       provided=None,
                       namespace=None,
                       container_ntiids=None,
                       container_all_of=True):
        query = {}
        container_query = 'all_of' if container_all_of else 'any_of'
        # prepare query
        for index, value, index_query in ((IX_SITE, sites, 'any_of'),
                                          (IX_NTIID, ntiid, 'any_of'),
                                          (IX_TYPE, provided, 'any_of'),
                                          (IX_TARGET, target, 'any_of'),
                                          (IX_MIMETYPE, mimetype, 'any_of'),
                                          (IX_NAMESPACE, namespace, 'any_of'),
                                          (IX_CONTAINERS, container_ntiids, container_query)):
            if value is not None:
                value = to_iterable(value)
                query[index] = {index_query: value}
        # query catalog
        result = self.apply(query)
        return result if result is not None else self.family.IF.LFSet()

    def search_objects(self,
                       ntiid=None,
                       sites=None,
                       target=None,
                       mimetype=None,
                       provided=None,
                       namespace=None,
                       container_ntiids=None,
                       container_all_of=True,
                       intids=None):
        intids = component.queryUtility(IIntIds) if intids is None else intids
        if intids is not None:
            refs = self.get_references(ntiid=ntiid,
                                       sites=sites,
                                       target=target,
                                       mimetype=mimetype,
                                       provided=provided,
                                       namespace=namespace,
                                       container_ntiids=container_ntiids,
                                       container_all_of=container_all_of)
            result = ResultSet(refs, intids)
        else:
            result = ()
        return result


def get_assets_catalog(registry=component):
    return registry.queryUtility(ICatalog, name=ASSETS_CATALOG_INDEX_NAME)


def create_assets_library_catalog(catalog=None, family=BTrees.family64):
    catalog = AssetsLibraryCatalog() if catalog is None else catalog
    for name, clazz in ((IX_SITE, SiteIndex),
                        (IX_TYPE, TypeIndex),
                        (IX_NTIID, NTIIDIndex),
                        (IX_TARGET, TargetIndex),
                        (IX_MIMETYPE, MimeTypeIndex),
                        (IX_NAMESPACE, NamespaceIndex),
                        (IX_CONTAINERS, ContainersIndex),
                        (IX_SLIDEDECK_VIDEOS, SlideDeckVideosIndex)):
        index = clazz(family=family)
        locate(index, catalog, name)
        catalog[name] = index
    return catalog


def install_assets_library_catalog(site_manager_container, intids=None):
    lsm = site_manager_container.getSiteManager()
    intids = lsm.getUtility(IIntIds) if intids is None else intids
    catalog = get_assets_catalog(lsm)
    if catalog is not None:
        return catalog

    catalog = create_assets_library_catalog(family=intids.family)
    locate(catalog, site_manager_container, ASSETS_CATALOG_INDEX_NAME)
    intids.register(catalog)
    lsm.registerUtility(catalog,
                        provided=ICatalog,
                        name=ASSETS_CATALOG_INDEX_NAME)

    for index in catalog.values():
        intids.register(index)
    return catalog
