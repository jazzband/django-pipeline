.. _ref-storages:

========
Storages
========

Using with a custom storage
===========================

Pipeline use `Django Storage <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#storages>`_
to read, save and delete files, by default it use an improved ``StaticFilesStorage``.

You can provide your own via ``PIPELINE_STORAGE`` : ::

  PIPELINE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


Using with staticfiles
======================

Pipeline is providing a storage for `staticfiles app <https://docs.djangoproject.com/en/dev/howto/static-files/>`_,
to use it configure ``STATICFILES_STORAGE`` like so ::

  STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
  
And if you want versioning use ::

  STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

Pipeline is also providing a storage that play nicely with staticfiles app
particularly for development : ::

  PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
