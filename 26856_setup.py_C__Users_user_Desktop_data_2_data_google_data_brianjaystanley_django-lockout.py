#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = '0.1.1'

setup(name='django-lockout',
      version=version,
      description="cache-based Django app that locks out users after too "
      "many failed login attempts.",
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Security',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',],
      keywords='django cache security',
      author='Brian Jay Stanley',
      url='https://github.com/brianjaystanley/django-lockout',
      author_email='brian@brianjaystanley.com',
      license='MIT',
      packages=['lockout'],
      install_requires=['django',],
)


