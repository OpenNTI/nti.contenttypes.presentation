import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    "z3c.autoinclude.plugin": [
        'target = nti.dataserver.contenttypes',
    ],
}

TESTS_REQUIRE = [
    'nose',
    'nose-timer',
    'nose-pudb',
    'nose-progressive',
    'nose2[coverage_plugin]',
    'pyhamcrest',
    'nti.nose_traceback_info',
    'nti.testing'
]

setup(
    name='nti.contenttypes.presentation',
    version=VERSION,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Presentation Content Types",
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    license='Proprietary',
    keywords='Content Presentation',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['nti', 'nti.contenttypes'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'BTrees',
        'nti.base',
        'nti.coremetadata',
        'nti.dublincore',
        'nti.externalization',
        'nti.mimetype',
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
        'zope.catalog',
        'zope.component',
        'zope.container',
        'zope.deferredimport',
        'zope.dublincore',
        'zope.file',
        'zope.i18nmessageid',
        'zope.intid',
        'zope.interface',
        'zope.location',
        'zope.schema',
        'zope.security'
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    dependency_links=[],
    entry_points=entry_points
)
