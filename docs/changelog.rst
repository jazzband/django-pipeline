Changelog
=========

1.1.15.1
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
