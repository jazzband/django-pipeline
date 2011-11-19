.. _ref-compressors:

===========
Compressors
===========


YUI Compressor compressor
=========================

The YUI compressor use `yui-compressor <http://developer.yahoo.com/yui/compressor/>`_
for compressing javascript and stylesheets. 

To use it for your stylesheets add this to your ``PIPELINE_CSS_COMPRESSOR`` ::

  PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

To use it for your javascripts add this to your ``PIPELINE_JS_COMPRESSOR`` ::

  PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'


``PIPELINE_YUI_BINARY``
-----------------------

  Command line to execute for the YUI program.
  You will most likely change this to the location of yui-compressor on your system.
  
  Defaults to ``'/usr/local/bin/yuicompressor'``.
  
.. warning::
  Don't point to ``yuicompressor.jar`` directly, we expect to find a executable script.
    

``PIPELINE_YUI_CSS_ARGUMENTS``
------------------------------

  Additional arguments to use when compressing CSS.

  Defaults to ``''``.

``PIPELINE_YUI_JS_ARGUMENTS``
-----------------------------

  Additional arguments to use when compressing JavaScript.
  
  Defaults to ``''``.


Closure Compiler compressor
===========================

The Closure compressor use `Google Closure Compiler <http://code.google.com/closure/compiler/>`_
to compress javascripts.

To use it add this to your ``PIPELINE_JS_COMPRESSOR`` ::

  PIPELINE_JS_COMPRESSOR = (
    'pipeline.compressors.closure.ClosureCompressor',
  )


``PIPELINE_CLOSURE_BINARY``
---------------------------

  Command line to execute for the Closure Compiler program.
  You will most likely change this to the location of closure on your system.
  
  Default to ``'/usr/local/bin/closure'``

.. warning::
  Don't point to ``compiler.jar`` directly, we expect to find a executable script.


``PIPELINE_CLOSURE_ARGUMENTS``
------------------------------

  Additional arguments to use when closure is called.
  
  Default to ``''``


UglifyJS compressor
===================

The UglifyJS compressor use `UglifyJS <https://github.com/mishoo/UglifyJS/>`_ to
compress javascripts.

To use it add this to your ``PIPELINE_JS_COMPRESSOR`` ::

  PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'


``PIPELINE_UGLIFYJS_BINARY``
----------------------------

  Command line to execute for the Closure Compiler program.
  You will most likely change this to the location of closure on your system.
  
  Defaults to ``'/usr/local/bin/uglifyjs'``.

``PIPELINE_UGLIFYJS_ARGUMENTS``
-------------------------------

  Additional arguments to use when uglifyjs is called.
  
  Default to ``''``


JSMin compressor
================

The jsmin compressor use Douglas Crockford jsmin tool to
compress javascripts.

To use it add this to your ``PIPELINE_JS_COMPRESSOR`` ::

  PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'

CSSTidy compressor
==================

The CSStidy compressor use `CSStidy <http://csstidy.sourceforge.net/>`_ to compress
stylesheets.

To us it for your stylesheets add this to your ``PIPELINE_CSS_COMPRESSOR`` ::

  PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.csstidy.CSSTidyCompressor'

``PIPELINE_CSSTIDY_BINARY``
---------------------------

  Command line to execute for csstidy program.
  You will most likely change this to the location of csstidy on your system.
  
  Defaults to ``'/usr/local/bin/csstidy'``

``PIPELINE_CSSTIDY_ARGUMENTS``
------------------------------

  Additional arguments to use when csstidy is called.

  Default to ``'--template=highest'``


Write your own compressor class
===============================

To write your own compressor class, for example want to implement other types
of compressors.

All you need to do is to create a class that inherits from ``pipeline.compressors.CompressorBase``
and implements ``compress_css`` and/or a ``compress_js`` when needed.

Finally, add it to ``PIPELINE_CSS_COMPRESSOR`` or 
``PIPELINE_JS_COMPRESSOR`` settings (see :doc:`configuration` for more information).

Example
-------

A custom compressor for a imaginary compressor called jam ::

  from pipeline.compressors import CompressorBase
  
  class JamCompressor(CompressorBase):
    def compress_js(self, js):
      return jam.compress(js)
    
    def compress(self, css):
      return jam.compress(css)
  

Add it to your settings ::

  PIPELINE_CSS_COMPRESSOR = 'jam.compressors.JamCompressor'
  PIPELINE_JS_COMPRESSOR = 'jam.compressors.JamCompressor'
