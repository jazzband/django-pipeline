Changelog
=========

1.1.27
------

* Improve windows support.
* Add support for Django 1.2. Thanks to Balazs Kossovics.

1.1.26
------

* Fix unicode issue. Thanks to Adam Charnock.

1.1.25
------

* Add stylus compiler. Thanks to David Charbonnier.
* Fix git versioning. Thanks to David Charbonnier again.
* Allow to disable asset normalization. Thansk to Christian Hammond.

1.1.24
------

* Add deprecation warning on external urls
* Fix windows paths support.
* Don't try to pack externals package. Thanks to Cristian Andreica for the report.


1.1.23
------

* Improve compressors documentation.
* Allow to have no compressors. Thanks to Christian Hammond.
* Fix less compiler to support @import. Thanks to TK Kocheran.

1.1.22
------

* Fix google closure compiler verbose mode. Thanks to cgreene.
* Fix absolute_path generation. Thanks to cgreene and Chris Northwood. 

1.1.21
------

* Fix js template name generation when there is only one template. Thanks to Gerrdo Curiel for the report. 

1.1.20
------

* Fix less and sass compilers.
* Properly overwrite compiled file if it already exists. 

1.1.19
------

* Add python 2.5 support.
* Remove lessc default arguments.

1.1.18.1
--------

* Ensure we don't break for font-face hack and other esoteric CSS urls.

1.1.18
------

* Ensure we don't break font-face urls.

1.1.17
------

* Don't use verbose where it's not supported or source of error.
* Improve syncompress cache bsuting ability.

1.1.16
------

* Add a way to compress specific groups with ``synccompress`` command.

1.1.15.2
--------

* Fixing typo.

1.1.15
------

* Allow synccompress to only update version cache.

1.1.14.1
--------

* Fix bug when calculating relative_path.

1.1.14
------

* Ensure javascript templates code get compiled properly. 
* Use os.path.relpath() instead of the more error-prone string.replace() to find the relative path. Thanks to Luke Yu-Po Chen.

1.1.13
------

* Use ``storage.save`` in ``Packager``, to play nicely with exotic storage.

1.1.12
------

* Add configurable cache timeout. Thanks to Matt Dennewitz.
* Catch any exception coming from ``storage``.

1.1.11
------

* Add documentation on pipeline signals, see :doc:`signals`.
* Cache version calculations, speeding up template tags.
* Not assuming anymore that version identifier are sortable
  (beware if you have setup ``PIPELINE_VERSION_REMOVE_OLD`` to ``False``).

1.1.10
------

* Make ``synccompress`` command work as expect when ``PIPELINE_AUTO`` is set to ``False``.
* Add a way to compress a specific group with ``synccompress`` command.
* Raise ``CompilerError`` when ``PIPELINE`` is set to ``False``.


1.1.9
-----

* Play more nicely with staticfiles app via ``PipelineFinderStorage``,
  see :doc:`storages`.

1.1.8.1
-------

* Fix bug in asset absolute path rewriting.

1.1.8
-----

* Faster templates tags.
* Storage speed up.

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
