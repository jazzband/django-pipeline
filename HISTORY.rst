.. :changelog:

History
=======

1.4.7
=====

* Rename 6to5 settings to match the new name: "babel".
* Improve upgrade instructions. Thanks to Collin Stedman.
* Make compiler work with storage not implementing path. Thanks to Brad Pitcher.

1.4.6
=====

* Improve LESS adapter compatibility. Thanks to Wictor Olseryd.
* Fix ``PipelineFinder`` behavior. Thanks to Aleksey Porfirov.
* Small tests and code improvements.

1.4.5
=====

* Add ES6/6to5 compiler.
* Fix URL rewriter quote handling. Thanks to Josh Braegger.
* Improve ``FileSystemFinder``. Thanks to Jon Dufresne.

1.4.4.1
=======

* Remove ruby sass implementation specifics.
* Remove artefacts in package.

1.4.3
=====

* Remove tempdir storage location. Thanks to Kristian Glass.
* Make the SASS compiler compatible with more non-ruby SASS. Thanks to Corrado Primier.

1.4.2
=====

* Fix finder bug. Thanks to Quentin Pradet, Remi and Sam Kuehn for the report
* Update finders documentation. Thanks to Thomas Schreiber, Grégoire Astruc and Tobias Birmili for the report.

1.4.1
=====

* Fix storage logic. Thanks to Quentin Pradet for the report.

1.4.0
=====

* **BACKWARD INCOMPATIBLE** : Renamed templatetags library from ``compressed`` to ``pipeline``.
* **BACKWARD INCOMPATIBLE** : Renamed templatetag ``compressed_js`` to ``javascript``.
* **BACKWARD INCOMPATIBLE** : Renamed templatetag ``compressed_css`` to ``stylesheet``.
