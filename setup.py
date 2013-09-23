#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name = "Helmholtz",
    version = "0.3.0dev",
    packages = find_packages(),
    package_data = {},
    author = "Neuroinformatics research group, UNIC, CNRS",
    author_email = "andrew.davison@unic.cnrs-gif.fr",
    description = "A framework for creating neuroscience databases",
    long_description = """LONG DESCRIPTION GOES HERE""",
    license = "CeCILL http://www.cecill.info",
    keywords = "neuroscience database Django metadata",
    url = "http://www.dbunic.cnrs-gif.fr/helmholtz/",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Science/Research',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Framework :: Django',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Database'],
)

