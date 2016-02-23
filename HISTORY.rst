.. :changelog:

History
=======

1.6.6
=====

* Fix filtering-out of files which require a finder to locate.
* Allow compilers to override the output path.
* Fix error reporting when a compiler fails to execute.
* Fix IOErrors when running collectstatic with some nodejs-based compilers and
  compressors. Thanks to Frankie Dintino.
* Fix compatibility of unit tests when running on Windows. Thanks to Frankie
  Dintino.
* Add unit tests for compilers and compressors. Thanks to Frankie Dintino.

1.6.5
=====

* Fix Django < 1.8 compatibility. Thanks to David Trowbridge.
* Allow to disable collector during development. Thanks to Leonardo Orozco.

1.6.4
=====

* Fix compressor subprocess calls.

1.6.3
=====

* Fix compressor command flattening.

1.6.2
=====

* Remove subprocess32 usage since it breaks universal support.

1.6.1
=====

* Fix path quoting issues. Thanks to Chad Miller.
* Use subprocess32 package when possible.
* Documentation fixes. Thanks to Sławek Ehlert and Jannis Leidel.

1.6.0
=====

* Add full support for Django 1.9.
* Drop support for Django 1.7.
* Drop support for Python 2.6.
* **BACKWARD INCOMPATIBLE** : Change configuration settings.
