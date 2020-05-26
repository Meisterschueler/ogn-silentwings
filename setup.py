#!/usr/bin/env python3

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ogn-silentwings',
    version=0.1,
    description='A python module to connect the Open Glider Network with Silent Wings',
    long_description=long_description,
    url='https://github.com/glidernet/python-ogn-silentwings',
    author='Konstantin Gründger aka Meisterschueler, Dominic Spreitz aka dspreitz',
    author_email='kammermark@gmx.de',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='gliding ogn silent wings',
    packages=['ogn.{}'.format(package) for package in find_packages(where='ogn')],
    python_requires='>=3',
    install_requires=[
        'Flask==1.1.1',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-SQLAlchemy==2.4.2',
        'Flask-Migrate==2.5.2',
        'manage.py==0.2.10',
        'coreapi==2.3.3',
        'hal-codec==1.0.2',
        'ogn-client==0.9.6',
        'aerofiles==1.0.0',
    ],
    extras_require={
        'dev': [
            'nose==1.3.7',
            'coveralls==1.10.0',
            'flake8==3.7.8',
        ]
    },
    zip_safe=False
)
