.. :changelog:

History
=======

1.6.12
======

* Fix a bug with os.rename on windows. Thanks to @wismill
* Fix to view compile error if happens. Thanks to @brawaga

1.6.11
======

* Fix performance regression. Thanks to Christian Hammond.

1.6.10
======

* Added Django 1.10 compatiblity issues. Thanks to Austin Pua and Silvan Spross.
* Documentation improvements. Thanks to Chris Streeter.

1.6.9
=====

* Various build improvements.
* Improved setup.py classifiers. Thanks to Sobolev Nikita.
* Documentation improvements. Thanks to Adam Chainz.

1.6.8
=====

* Made templatetags easier to subclass for special rendering behavior. Thanks
  to Christian Hammond.
* Updated the link to readthedocs. Thanks to Corey Farwell.
* Fixed some log messages to correctly refer to the new PIPELINE settings
  tructure. Thanks to Alvin Mites.
* Changed file outdated checks to use os.path methods directly, avoiding
  potential SuspiciousFileOperation errors which could appear with some django
  storage configurations.

1.6.7
=====

* Add a view for collecting static files before serving them. This behaves like
  django's built-in ``static`` view and allows running the collector for
  images, fonts, and other static files that do not need to be compiled. Thanks
  to Christian Hammond.
* Update documentation for the ES6Compiler to clarify filename requirements.
  Thanks to Nathan Cox.
* Add error output for compiler errors within the browser. This provides for a
  much better experience when compiling files from the devserver. Thanks to
  Christian Hammond.
* Make unit tests run against Django 1.6 and 1.7. Thanks to Sławek Ehlert.

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
