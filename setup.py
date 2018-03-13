import codecs
from setuptools import setup
from setuptools import find_packages

entry_points = {
    "z3c.autoinclude.plugin": [
        'target = nti.dataserver.contenttypes',
    ],
}

TESTS_REQUIRE = [
    'fudge',
    'nti.testing',
    'zope.formlib',
    'zope.dottedname',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.contenttypes.presentation',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Presentation Content Types",
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read("CHANGES.rst")
    ),
    license='Apache',
    keywords='Content Presentation',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/NextThought/nti.contenttypes.presentation",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti', 'nti.contenttypes'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'BTrees',
        'nti.base',
        'nti.containers',
        'nti.contenttypes.completion',
        'nti.contenttypes.reports',
        'nti.coremetadata',
        'nti.dublincore',
        'nti.externalization',
        'nti.mimetype',
        'nti.namedfile',
        'nti.ntiids',
        'nti.property',
        'nti.publishing',
        'nti.recorder',
        'nti.schema',
        'nti.wref',
        'nti.zodb',
        'nti.zope_catalog',
        'six',
        'persistent',
        'zc.catalog',
        'ZODB',
        'zope.annotation',
        'zope.cachedescriptors',
        'zope.catalog',
        'zope.component',
        'zope.container',
        'zope.deferredimport',
        'zope.deprecation',
        'zope.dublincore',
        'zope.file',
        'zope.i18nmessageid',
        'zope.intid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.mimetype',
        'zope.schema',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
            'zope.formlib',
        ],
    },
    entry_points=entry_points,
)
