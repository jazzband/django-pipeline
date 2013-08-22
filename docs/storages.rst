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
