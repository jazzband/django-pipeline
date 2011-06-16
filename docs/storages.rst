.. _ref-storages:

========
Storages
========

Using with a custom storage
===========================

Pipeline use `Django Storage <https://docs.djangoproject.com/en/dev/ref/files/storage/>`_
to read, save and delete files, by default it use an improved ``FileSystemStorage``.

You can provide your own via ``PIPELINE_STORAGE`` : ::

  PIPELINE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


Using with staticfiles
======================

Pipeline is providing a Finder for `staticfiles app <https://docs.djangoproject.com/en/dev/howto/static-files/>`_,
to use it configure ``STATICFILES_FINDERS`` like so : ::

  STATICFILES_FINDERS = 'pipeline.finders.PipelineFinder'

