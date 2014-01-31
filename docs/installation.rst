.. _ref-installation:

============
Installation
============

1. Either check out Pipeline from GitHub_ or to pull a release off PyPI_ ::

       pip install django-pipeline


2. Add 'pipeline' to your ``INSTALLED_APPS`` ::

       INSTALLED_APPS = (
           'pipeline',
       )

3. Use a pipeline storage for ``STATICFILES_STORAGE`` ::

        STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


.. note::
  You need to use ``Django>=1.5`` to be able to use this version of pipeline.

.. _GitHub: http://github.com/cyberdelia/django-pipeline
.. _PyPI: http://pypi.python.org/pypi/django-pipeline

Recommendations
===============

Pipeline's default CSS and JS compressor is Yuglify.
Yuglify wraps UglifyJS and cssmin, applying the default YUI configurations to them.
It can be downloaded from: https://github.com/yui/yuglify/.

If you do not install yuglify, make sure to disable the compressor in your settings.

