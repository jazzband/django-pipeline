.. :changelog:

History
=======

Unreleased
==========

* Moving tests to GitHub Actions: https://github.com/jazzband/django-pipeline/actions

2.0.5
======

* Adding **Django 3.1** compatibility.
* CachedStaticFilesStorage is removed from Django. Add a check
  of the current version to prevent error while importing. Thank to @vmsp
* Context in django.template.base is removed from Django and
  not used anymore in django-pipeline.
* Fixing widgets tests of django-pipeline due to Media.render_js change in 
  Django. More information in Django ticket #31892

2.0.4
======

* Adding **css-html-js-minify** support to compress JS and CSS.
* Update compressors documentation with css-html-js-minify.
* Create tests for css-html-js-minify compressor.
* Optimization by grouping the tests yuglify compressor.

2.0.3
======

* Remove futures from pipeline **setup.py** requirements.

2.0.2
=====

* Fix Middleware to properly decode HTML. Thank to @gatsinski
* Keep mimetypes as str. Thank to @benspaulding
* Based on #642 add 'NonPackagingPipelineManifestStorage' and update
  the documentation: **storages.rst**. Thank to @kronion

2.0.1
=====

* Add subclass of ManifestStaticFilesStorage. Thank to @jhpinson
* Change the documentation to use PipelineManifestStorage in configuration
  instead of PipelineCachedStorage now deprecated.
* Change import MutableMapping from collections.abc. Thank to @colons

2.0.0
=====

* **Definitely drop the support of Python 2**.
* Drop support for Python 3.5 (not compatible with PEP 498).
* Remove 'decorator.py' how was used for backward compatibility
  between python 2 and 3 for metaclass inheritance on PipelineFormMedia.
* Replace 'format' by 'fstring' (PEP 498: Literal String Interpolation).
* Remove of old imports form 'django.utils.six' and these fixes (1.7.0).
* Remove tests of uncovered versions of Python and Django.
* Replace tests for Pypy by Pypy3.
* Explicitly specify when files are read / write in binary mode.
* Set opening files for tests to deal with universal newlines.
* Upgrade documentation version to 2.0 to follow the project version.

1.7.0
=====

* Release the last major version of django-pipeline working on Python 2.
* Thank you for all the modifications made since version 1.6.14, which we cannot quote.
* Apply an optimization to save time during development. Thank to @blankser
* Edit setup.py to follow the recommendation of the documentation. Thank to @shaneikennedy
* Add tests for Django 3.0 and Python 3.8
* Add alternatives imports for django.utils.six, who has been removed in Django 3.0

1.6.14
======

* Fix packaging issues.

1.6.13
======

* Fix forward-slashed paths on Windows. Thanks to @etiago
* Fix CSS URL detector to match quotes correctly. Thanks to @vskh
* Add a compiler_options dict to compile, to allow passing options to custom
  compilers. Thanks to @sassanh
* Verify support for Django 1.11. Thanks to @jwhitlock

1.6.12
======

* Supports Django 1.11
* Fix a bug with os.rename on windows. Thanks to @wismill
* Fix to view compile error if happens. Thanks to @brawaga
* Add support for Pipeline CSS/JS packages in forms and widgets. Thanks to @chipx86

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
