.. :changelog:

History
=======


1.1.23
------

* Separate yuglify compressor from YUI compressor.
* Improve HTML compression middleware.


1.1.22
------

* Better compressor error messages. Thanks to Steven Cummings.
* Improve installation documentation. Thanks to Steven Cummings.
* Fix packaging metadata. Thanks to Rui Coelho for noticing it.
* Add documentation about non-packing storage.

1.1.21
------

* Run stylus even if file is considered outdated.

1.1.20
------

* Ensure yui-compressor can still use YUICompressor.

1.2.19
------

* **BACKWARD INCOMPATIBLE** : Replace python cssmin compressor to run the command (works for python or node implementation)

1.2.18
------

* **BACKWARD INCOMPATIBLE** : Replace yui-compressor by yuglify, check your configuration.
* Use finders in manifest. Thanks to Sjoerd Arendsen.

1.2.17
------

* Fully tested windows compatibility. Thanks to Idan Zalzberg.

1.2.16
------

* Fix manifesto module. Thanks to Zenobius Jiricek.
* Ensure coffee-script compiler don't try to overwrite file. Thanks to Teo Klestrup Röijezon.

1.2.15
------

* Ensure asset url are build with ``posixpath``.
* Deal with storage prefix properly.

1.2.14
------

* Jinja2 support, thanks to Christopher Reeves.
* Add read/save_file method to CompilerBase.

1.2.13
------

* Fix unicode bug in compressor. Thanks to Victor Shnayder.
* Fix outdated detection bug. Thanks to Victor Shnayder and Erwan Ameil.
* Add slimit compressor. Thanks to Brant Young.

1.2.12
------

* Fix IO error when creating new compiled file. Thanks to Melvin Laplanche.

1.2.11
------

* Add a small contribution guide
* Add mimetype settings for sass and scss
* Change compiler interface to let compiler determine if file is outdated

1.2.10
------

* Use ``/usr/bin/env`` by default to find compiler executable. Thanks to Michael Weibel.
* Allow to change embed settings : max size and directory. Thanks to Pierre Drescher.
* Some documentation improvements. Thanks to Florent Messa.

1.2.9
-----

* Don't compile non-outdated files.
* Add non-packing storage.

1.2.8
-----

* Fix bugs in our glob implementation.


1.2.7
-----

* Many documentation improvements. Thanks to Alexis Svinartchouk.
* Improve python packaging.
* Don't write silently to STATIC_ROOT when we shouldn't.
* Accept new .sass extension in SASSCompiler. Thanks to Jonas Geiregat for the report.


1.2.6
-----

* New lines in templates are now escaper rather than deleted. Thanks to Trey Smith for the report and the patch.
* Improve how we find where to write compiled file. Thanks to sirex for the patch.


1.2.5
-----

* Fix import error for cssmin and jsmin compressors. Thanks to Berker Peksag for the report.
* Fix error with default template function. Thanks to David Charbonnier for the patch and report.


1.2.4
-----

* Fix encoding problem.
* Improve storage documentation
* Add mention of the IRC channel #django-pipeline in documentation


1.2.3
-----

* Fix javascript mime type bug. Thanks to Chase Seibert for the report.


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
