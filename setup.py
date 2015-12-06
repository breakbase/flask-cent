'''
    Flask-Cent
    -----------

    Flask-Cent is a flask extension for centrifugal/cent
'''
import os
import sys

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_cent.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

setup(name='Flask-Cent',
      version=__version__,
      url='https://github.com/breakbase/flask-cent',
      license='MIT',
      author="BreakBase.com",
      author_email='oss@breakbase.com',
      description='centrifugal/cent client for flask',
      long_description=__doc__,
      py_modules=['flask_cent'],
      zip_safe=False,
      platforms='any',
      test_suite='nose.collector',
      install_requires=[
          'Flask',
          'blinker',
      ],
      tests_require=[
          'nose',
          'blinker',
          'speaklater',
          'mock',
      ],
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ])
