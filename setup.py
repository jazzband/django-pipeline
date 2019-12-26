# -*- coding: utf-8 -*-
import io

from setuptools import setup, find_packages
import sys

setup(
    name='django-pipeline',
    version='1.7.0',
    description='Pipeline is an asset packaging library for Django.',
    long_description=io.open('README.rst', encoding='utf-8').read() + '\n\n' +
        io.open('HISTORY.rst', encoding='utf-8').read(),
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/jazzband/django-pipeline',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.tests']),
    zip_safe=False,
    install_requires=['futures >= 2.1.3;python_version<"3"'],
    include_package_data=True,
    keywords=('django pipeline asset compiling concatenation compression'
              ' packaging'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
