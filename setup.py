# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-pipeline',
    version='1.2.18',
    description='Pipeline is an asset packaging library for Django.',
    long_description=open('README.rst').read() + '\n\n' +
        open('HISTORY.rst').read(),
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/django-pipeline',
    license=open('LICENSE').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
