import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.1.1'
requires = []

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='powerlibs-django-contrib-eventful',
    version=version,
    description="Django models that serve as base for event based actions",
    long_description=readme,
    author='Cléber Zavadniak',
    author_email='cleberman@gmail.com',
    url='https://github.com/Dronemapp/powerlibs-django-contrib-eventful',
    license=license,
    packages=['powerlibs.django.contrib.eventful'],
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    keywords='generic libraries',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)
