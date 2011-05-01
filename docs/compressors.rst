.. _ref-compressors:

===========
Compressors
===========

Template tags
=============

If you need to change the output of the HTML-tags generated from the templatetags,
this can be done by overriding the templates ``compress/css.html`` and ``compress/js.html``.


YUI Compressor compressor
=========================

The YUI compressor use `yui-compressor <http://developer.yahoo.com/yui/compressor/>`_
for compressing javascript and stylesheets. 

To us it for your stylesheets add this to your ``COMPRESS_CSS_COMPRESSORS`` ::

  COMPRESS_CSS_COMPRESSORS = (
    'compress.compressors.yui.YUICompressor',
  )

To use it for your javascripts add this to your ``COMPRESS_JS_COMPRESSORS`` ::

  COMPRESS_JS_COMPRESSORS = (
    'compress.compressors.yui.YUICompressor',
  )


``COMPRESS_YUI_BINARY``
-----------------------

  Command line to execute for the YUI program.
  You will most likely change this to the location of yui-compressor on your system.
  
  Defaults to ``'/usr/local/bin/yuicompressor'``.

``COMPRESS_YUI_CSS_ARGUMENTS``
------------------------------

  Additional arguments to use when compressing CSS.

  Defaults to ``''``.

``COMPRESS_YUI_JS_ARGUMENTS``
-----------------------------

  Additional arguments to use when compressing JavaScript.
  
  Defaults to ``''``.


Closure Compiler compressor
===========================

The Closure compressor use `Google Closure Compiler <http://code.google.com/closure/compiler/>`_
to compress javascripts.

To use it add this to your ``COMPRESS_JS_COMPRESSORS`` ::

  COMPRESS_JS_COMPRESSORS = (
    'compress.compressors.closure.ClosureCompressor',
  )


``COMPRESS_CLOSURE_BINARY``
---------------------------

  Command line to execute for the Closure Compiler program.
  You will most likely change this to the location of closure on your system.
  
  Default to ``'/usr/local/bin/closure'``

``COMPRESS_CLOSURE_ARGUMENTS``
------------------------------

  Additional arguments to use when closure is called.
  
  Default to ``''``


UglifyJS compressor
===================

The UglifyJS compressor use `UglifyJS <https://github.com/mishoo/UglifyJS/>`_ to
compress javascripts.

To use it add this to your ``COMPRESS_JS_COMPRESSORS`` ::

  COMPRESS_JS_COMPRESSORS = (
    'compress.compressors.uglifyjs.UglifyJSCompressor',
  )


``COMPRESS_UGLIFYJS_BINARY``
----------------------------

  Command line to execute for the Closure Compiler program.
  You will most likely change this to the location of closure on your system.
  
  Defaults to ``'/usr/local/bin/uglifyjs'``.

``COMPRESS_UGLIFYJS_ARGUMENTS``
-------------------------------

  Additional arguments to use when uglifyjs is called.
  
  Default to ``''``


JSMin compressor
================

The jsmin compressor use Douglas Crockford jsmin tool to
compress javascripts.

To use it add this to your ``COMPRESS_JS_COMPRESSORS`` ::

  COMPRESS_JS_COMPRESSORS = (
    'compress.compressors.jsmin.JSMinCompressor',
  )

CSSTidy compressor
==================

The CSStidy compressor use `CSStidy <http://csstidy.sourceforge.net/>`_ to compress
stylesheets.

To us it for your stylesheets add this to your ``COMPRESS_CSS_COMPRESSORS`` ::

  COMPRESS_CSS_COMPRESSORS = (
    'compress.compressors.csstidy.CSSTidyCompressor',
  )

``COMPRESS_CSSTIDY_BINARY``
---------------------------

  Command line to execute for csstidy program.
  You will most likely change this to the location of csstidy on your system.
  
  Defaults to ``'/usr/local/bin/csstidy'``

``COMPRESS_CSSTIDY_ARGUMENTS``
------------------------------

  Additional arguments to use when csstidy is called.

  Default to ``'--template=highest'``


Write your own compressor class
===============================

To write your own compressor class, for example want to implement other types
of compressors.

All you need to do is to create a class that inherits from ``compress.compressors.CompressorBase``
and implements ``compress_css`` and/or a ``compress_js`` when needed.

Finally, specify it in the tuple of compressors ``COMPRESS_CSS_COMPRESSORS`` or 
``COMPRESS_JS_COMPRESSORS`` (see :doc:`configuration` for more information) in the settings.

Example
-------

A custom compressor for a imaginary compressor called jam ::

  from compress.compressors import CompressorBase
  
  class JamCompressor(CompressorBase):
    def compress_js(self, js):
      return jam.compress(js)
    
    def compress(self, css):
      return jam.compress(css)
  
