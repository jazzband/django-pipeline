.. _ref-storages:

========
Storages
========


Using with staticfiles
======================

Pipeline is providing a storage for `staticfiles app <https://docs.djangoproject.com/en/dev/howto/static-files/>`_,
to use it configure ``STATICFILES_STORAGE`` like so ::

  STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

And if you want versioning use ::

  STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

There is also non-packing storage available, that allows you to run ``collectstatic`` command
without packaging your assets. Useful for production when you don't want to run compressor or compilers ::

  STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

Also available if you want versioning ::

  STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineCachedStorage'

If you use staticfiles with ``DEBUG = False`` (i.e. for integration tests
with `Selenium <http://docs.seleniumhq.org/>`_) you should install the finder
that allows staticfiles to locate your outputted assets : ::

  STATICFILES_FINDERS = (
      'django.contrib.staticfiles.finders.FileSystemFinder',
      'django.contrib.staticfiles.finders.AppDirectoriesFinder',
      'pipeline.finders.PipelineFinder',
  )

If you use ``PipelineCachedStorage`` you may also like the ``CachedFileFinder``,
which allows you to use integration tests with cached file URLs.

If you want to exclude Pipelinable content from your collected static files,
you can also use Pipeline's ``FileSystemFinder`` and ``AppDirectoriesFinder``.
These finders will also exclude `unwanted` content like READMEs, tests and
examples, which are particularly useful if you're collecting content from a
tool like Bower. ::

  STATICFILES_FINDERS = (
      'pipeline.finders.FileSystemFinder',
      'pipeline.finders.AppDirectoriesFinder',
      'pipeline.finders.PipelineFinder',
      'pipeline.finders.CachedFileFinder',
  )

GZIP compression
================

Pipeline can also creates a gzipped version of your collected static files,
so that you can avoid compressing them on the fly. ::

  STATICFILES_STORAGE = 'your.app.GZIPCachedStorage'

The storage need to inherit from ``GzipMixin``: ::

  from staticfiles.storage import CachedStaticFilesStorage

  from pipeline.storage import GZIPMixin


  class GZIPCachedStorage(GZIPMixin, CachedStaticFilesStorage):
      pass


Using with other storages
=========================

You can also use your own custom storage, for example, if you want to use S3 for your assets : ::

  STATICFILES_STORAGE = 'your.app.S3PipelineStorage'

Your storage only need to inherit from ``PipelineMixin`` and/or ``CachedFilesMixin`` : ::

  from staticfiles.storage import CachedFilesMixin

  from pipeline.storage import PipelineMixin

  from storages.backends.s3boto import S3BotoStorage


  class S3PipelineStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
      pass

Using Pipeline with Bower
=========================

`Bower <http://bower.io/>`_ is a `package manager for the web` that allows
you to easily include frontend components with named versions. Integrating
Bower with Pipeline is straightforward.

Add your Bower directory to your ``STATICFILES_DIRS`` : ::

  STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'bower_components'),
  )

Then process the relevant content through Pipeline : ::

  PIPELINE_JS = {
    'components': {
      'source_filenames: (
        'jquery/jquery.js',
        # you can choose to be specific to reduce your payload
        'jquery-ui/ui/*.js',
      ),
      'output_filename': 'js/components.js',
    },
  }

``pipeline.finders.FileSystemFinder`` will help you by excluding much of the
extra content that Bower includes with its components, such as READMEs, tests
and examples, while still including images, fonts, CSS fragments etc.
