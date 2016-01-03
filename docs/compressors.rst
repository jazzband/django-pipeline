.. _ref-compressors:

===========
Compressors
===========


Yuglify compressor
==================

The Yuglify compressor uses `yuglify <http://github.com/yui/yuglify>`_
for compressing javascript and stylesheets.

To use it for your stylesheets add this to your ``PIPELINE['CSS_COMPRESSOR']`` ::

  PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'

To use it for your javascripts add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'


``YUGLIFY_BINARY``
---------------------------

  Command line to execute for the Yuglify program.
  You will most likely change this to the location of yuglify on your system.

  Defaults to ``'/usr/bin/env yuglify'``.

``YUGLIFY_CSS_ARGUMENTS``
----------------------------------

  Additional arguments to use when compressing CSS.

  Defaults to ``'--terminal'``.

``YUGLIFY_JS_ARGUMENTS``
---------------------------------

  Additional arguments to use when compressing JavaScript.

  Defaults to ``'--terminal'``.


YUI Compressor compressor
=========================

The YUI compressor uses `yui-compressor <http://developer.yahoo.com/yui/compressor/>`_
for compressing javascript and stylesheets.

To use it for your stylesheets add this to your ``PIPELINE['CSS_COMPRESSOR']`` ::

  PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'

To use it for your javascripts add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'


``YUI_BINARY``
-----------------------

  Command line to execute for the YUI program.
  You will most likely change this to the location of yui-compressor on your system.

  Defaults to ``'/usr/bin/env yuicompressor'``.

.. warning::
  Don't point to ``yuicompressor.jar`` directly, we expect to find a executable script.


``YUI_CSS_ARGUMENTS``
------------------------------

  Additional arguments to use when compressing CSS.

  Defaults to ``''``.

``YUI_JS_ARGUMENTS``
-----------------------------

  Additional arguments to use when compressing JavaScript.

  Defaults to ``''``.


Closure Compiler compressor
===========================

The Closure compressor uses `Google Closure Compiler <http://code.google.com/closure/compiler/>`_
to compress javascripts.

To use it add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.closure.ClosureCompressor'


``CLOSURE_BINARY``
---------------------------

  Command line to execute for the Closure Compiler program.
  You will most likely change this to the location of closure on your system.

  Default to ``'/usr/bin/env closure'``

.. warning::
  Don't point to ``compiler.jar`` directly, we expect to find a executable script.


``CLOSURE_ARGUMENTS``
------------------------------

  Additional arguments to use when closure is called.

  Default to ``''``


UglifyJS compressor
===================

The UglifyJS compressor uses `UglifyJS <https://github.com/mishoo/UglifyJS2/>`_ to
compress javascripts.

To use it add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'


``UGLIFYJS_BINARY``
----------------------------

  Command line to execute for the UglifyJS program.
  You will most likely change this to the location of uglifyjs on your system.

  Defaults to ``'/usr/bin/env uglifyjs'``.

``UGLIFYJS_ARGUMENTS``
-------------------------------

  Additional arguments to use when uglifyjs is called.

  Default to ``''``


JSMin compressor
================

The jsmin compressor uses Douglas Crockford jsmin tool to
compress javascripts.

To use it add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.jsmin.JSMinCompressor'

Install the jsmin library with your favorite Python package manager ::

  pip install jsmin


SlimIt compressor
=================

The slimit compressor uses `SlimIt <http://slimit.readthedocs.org>`_ to
compress javascripts.

To use it add this to your ``PIPELINE['JS_COMPRESSOR']`` ::

  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.slimit.SlimItCompressor'

Install the slimit library with your favorite Python package manager ::

  pip install slimit


CSSTidy compressor
==================

The CSStidy compressor uses `CSStidy <http://csstidy.sourceforge.net/>`_ to compress
stylesheets.

To us it for your stylesheets add this to your ``PIPELINE['CSS_COMPRESSOR']`` ::

  PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.csstidy.CSSTidyCompressor'

``CSSTIDY_BINARY``
---------------------------

  Command line to execute for csstidy program.
  You will most likely change this to the location of csstidy on your system.

  Defaults to ``'/usr/bin/env csstidy'``

``CSSTIDY_ARGUMENTS``
------------------------------

  Additional arguments to use when csstidy is called.

  Default to ``'--template=highest'``

CSSMin compressor
=================

The cssmin compressor uses the `cssmin <https://github.com/jbleuzen/node-cssmin>`_
command to compress stylesheets. To use it, add this to your ``PIPELINE['CSS_COMPRESSOR']`` ::

  PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.cssmin.CSSMinCompressor'

``CSSMIN_BINARY``
---------------------------

  Command line to execute for cssmin program.
  You will most likely change this to the location of cssmin on your system.

  Defaults to ``'/usr/bin/env cssmin'``

``CSSMIN_ARGUMENTS``
------------------------------

  Additional arguments to use when cssmin is called.

  Default to ``''``

No-Op Compressors
=================

The No-Op compressor don't perform any operation, when used, only concatenation occurs.
This is useful for debugging faulty concatenation due to poorly written javascript and other errors.

To use it, add this to your settings ::

  PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.NoopCompressor'
  PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.NoopCompressor'


Write your own compressor class
===============================

You can write your own compressor class, for example if you want to implement other types
of compressors.

To do so, you just have to create a class that inherits from ``pipeline.compressors.CompressorBase``
and implements ``compress_css`` and/or a ``compress_js`` when needed.

Finally, add it to ``PIPELINE['CSS_COMPRESSOR']`` or
``PIPELINE['JS_COMPRESSOR']`` settings (see :doc:`configuration` for more information).

Example
-------

A custom compressor for an imaginary compressor called jam ::

  from pipeline.compressors import CompressorBase

  class JamCompressor(CompressorBase):
    def compress_js(self, js):
      return jam.compress(js)

    def compress_css(self, css):
      return jam.compress(css)


Add it to your settings ::

  PIPELINE['CSS_COMPRESSOR'] = 'jam.compressors.JamCompressor'
  PIPELINE['JS_COMPRESSOR'] = 'jam.compressors.JamCompressor'
