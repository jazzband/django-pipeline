.. _ref-installation:

============
Installation
============

1. Either check out django-compress from GitHub_ or to pull a release off PyPI_ ::
   
       pip install django-compress
    

2. Add 'compress' to your ``INSTALLED_APPS`` ::

       INSTALLED_APPS = (
           'compress',
       )


.. _GitHub: http://github.com/pelme/django-compress
.. _PyPI: http://pypi.python.org/

Recommendations
===============

By default django-compress uses YUI Compressor to compress CSS and JS.
YUI Compressor is an excellent stand-alone application for dealing with JS and CSS-files.
YUI Compressor can be downloaded from: http://developer.yahoo.com/yui/compressor/.

If you do not install YUI COMPRESSOR, make sure to disable the compressor in your settings.
