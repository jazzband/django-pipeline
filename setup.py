# -*- coding: utf-8 -*-
import io

from setuptools import setup, find_packages
import sys

install_requires = []
if (sys.version_info[0], sys.version_info[1]) < (3, 2):
    install_requires.append('futures>=2.1.3')

setup(
    name='django-pipeline',
    version='1.6.13',
    description='Pipeline is an asset packaging library for Django.',
    long_description=io.open('README.rst', encoding='utf-8').read() + '\n\n' +
        io.open('HISTORY.rst', encoding='utf-8').read(),
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/jazzband/django-pipeline',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    keywords=('django pipeline asset compiling concatenation compression'
              ' packaging'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
