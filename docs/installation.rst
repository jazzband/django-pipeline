.. _ref-installation:

============
Installation
============

1. Either check out Pipeline from GitHub_ or to pull a release off PyPI_ ::
   
       pip install django-pipeline
    

2. Add 'compress' to your ``INSTALLED_APPS`` ::

       INSTALLED_APPS = (
           'pipeline',
       )


.. _GitHub: http://github.com/cyberdelia/django-pipeline
.. _PyPI: http://pypi.python.org/pypi/django-pipeline

Recommendations
===============

By default Pipeline uses YUI Compressor to compress CSS and JS.
YUI Compressor is an excellent stand-alone application for dealing with JS and CSS-files.
YUI Compressor can be downloaded from: http://developer.yahoo.com/yui/compressor/.

If you do not install YUI Compressor, make sure to disable the compressor in your settings.
