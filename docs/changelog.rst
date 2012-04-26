Changelog
=========


1.2.2.1
-------

* License clarification. Thanks to Dmitry Nezhevenko for the report.


1.2.2
-----

* Allow to disable javascript closure wrapper with ``PIPELINE_DISABLE_WRAPPER``.
* Various improvements to documentation.
* Slightly improve how we find where to write compiled file.
* Simplify module hierarchy.
* Allow templatetag to output mimetype to be able to use less.js and other javascript compilers.


1.2.1
-----

* Fixing a bug in ``FinderStorage`` when using prefix in staticfiles. Thanks to Christian Hammond for the report and testing.
* Make ``PIPELINE_ROOT`` defaults more sane. Thanks to Konstantinos Pachnis for the report.


1.2.0
-----

* Dropped ``synccompress`` command in favor of staticfiles ``collecstatic`` command.
* Added file versionning via staticfiles ``CachedStaticFilesStorage``.
* Added a default js template language.
* Dropped ``PIPELINE_AUTO`` settings in favor of simple ``PIPELINE``.
* Renamed ``absolute_asset_paths`` to ``absolute_paths`` for brevity.
* Made packages lazy to avoid doing unnecessary I/O. 
* Dropped ``external_urls`` support for now.
* Add cssmin compressor. Thanks to Steven Cummings.
* Jsmin is no more bundle with pipeline.
