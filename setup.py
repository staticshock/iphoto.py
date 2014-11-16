#!/usr/bin/env python
from setuptools import setup

setup(
    name='iphoto',
    version='0.1.0',
    description='Command line interface to iPhoto',
    long_description=open("README.rst").read(),
    author='Anton Backer',
    author_email='olegov@gmail.com',
    url='http://www.github.com/staticshock/iphoto.py',
    packages=['iphoto'],
    install_requires=['sqlalchemy', 'click'],
    entry_points=dict(
        console_scripts=['iphoto = iphoto.cli:main'],
    ),
    license='ISC',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    )
)
