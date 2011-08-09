Changelog
=========

1.1.9
-----

* Play more nicely with staticfiles app via ``PipelineFinderStorage``,
  see :doc:`storages`.

1.1.8.1
-------

* Fix bug in asset absolute path rewriting.

1.1.8
-----

* Faster templates tags
* Storage speed up

1.1.7
-----

* Improved windows support. Thanks to Kyle MacFarlane.
* Added Manifesto support.

1.1.0
-----

* Most of the settings name have change to be prefixed by ``PIPELINE_``.
* CSSTidy isn't the default anymore, YUI Compressor is now the default.
* Filters are now called compressors.
* You can only specify one compressor via ``PIPELINE_CSS_COMPRESSOR`` or
  ``PIPELINE_JS_COMPRESSOR``
