.. _ref-configuration:

=============
Configuration
=============


Configuration and list of available settings for Pipeline


Specifying files
================

You specify groups of files to be compressed in your settings. You can use glob 
syntax to select multiples files.

The basic syntax for specifying CSS/JavaScript groups files is ::

  PIPELINE_CSS = {
      'colors': {
          'source_filenames': (
            'css/core.css',
            'css/colors/*.css',
            'css/layers.css'
          ),
          'output_filename': 'css/colors.css',
          'extra_context': {
              'media': 'screen,projection',
          },
      },
  }

  PIPELINE_JS = {
      'stats': {
          'source_filenames': (
            'js/jquery.js',
            'js/d3.js',
            'js/collections/*.js',
            'js/application.js',
          ),
          'output_filename': 'js/stats.js',
      }
  }

Group options
-------------

``source_filenames``
....................

  **Required**
  
  Is a tuple with the source files to be compressed.
  The files are concatenated in the order it is specified in the tuple.
  

``output_filename``
...................
 
  **Required**
 
  Is the filename of the (to be) compressed file.

``variant``
...........

  **Optional**
  
  Is the variant you want to apply to your CSS. This allow you to embed images
  and fonts in CSS with data-URI.
  Allowed values are : ``None`` and ``datauri``.
  
  Defaults to ``None``.

``template_name``
.................

  **Optional**
  
  Name of the template used to render ``<script>`` for js package or ``<link>`` for css package.
  
  Defaults to ``None``.

``extra_context``
.................

  **Optional**
  
  Is a dictionary of values to add to the template context,
  when generating the HTML for the HTML-tags with the templatetags.
  
  For CSS, if you do not specify ``extra_context``/``media``, the default media in
  the ``<link>`` output will be ``media="all"``.

``manifest``
............

  **Optional**

  Indicate if you want this group to appear in your cache manifest.

  Defaults to ``True``.


Other settings
--------------

``PIPELINE``
............

  When ``PIPELINE`` is ``True``, CSS and JavaScripts will be concatenated and filtered.
  When ``False``, the source-files will be used instead.

  Defaults to ``not DEBUG`` (compressed files will only be used when ``DEBUG`` is ``False``).

``PIPELINE_CSS_COMPRESSOR``
............................

  Compressor class to be applied to CSS files.

  If empty or ``None``, CSS files won't be compressed.
  
  Defaults to ``'pipeline.compressors.yui.YUICompressor'``.

``PIPELINE_JS_COMPRESSOR``
...........................

  Compressor class to be applied to JavaScript files.

  If empty or ``None``, JavaScript files won't be compressed.
  
  Defaults to ``'pipeline.compressors.yui.YUICompressor'``

.. note::

  Please note that in order to use YUI Compressor, you need to install YUI Compressor (see :doc:`installation` for more details).

``PIPELINE_TEMPLATE_NAMESPACE``
...............................

  Object name where all of your compiled templates will be added, from within your browser.
  To access them with your own JavaScript namespace, change it to the object of your choice.

  Defaults to ``"window.JST"``


``PIPELINE_TEMPLATE_EXT``
.........................

  The extension for which Pipeline will consider the file as a Javascript templates.
  To use a different extension, like ``.mustache``, set this settings to ``.mustache``.

  Defaults to ``".jst"``

``PIPELINE_TEMPLATE_FUNC``
..........................

  JavaScript function that compiles your JavaScript templates.
  Pipeline doesn't bundle a javascript template library, but the default
  settings is to use the
  `underscore <http://documentcloud.github.com/underscore/>`_ template function.
  
  Defaults to ``"_.template"``


Embedding fonts and images
==========================

You can embed fonts and images directly in your compiled css, using Data-URI in 
modern browser. 

To do so, setup variant group options to the method you wish to use : ::

  PIPELINE_CSS = {
      'master': {
          'source_filenames': (
            'css/core.css',
            'css/button/*.css',
          ),
          'output_filename': 'css/master.css',
          'variant': 'datauri',
      },
  }

Images and fonts are embedded following these rules :

- If asset is under **32 kilobytes** to avoid rendering delay or not rendering
  at all in Internet Explorer 8.
- If asset path contains a directory named "**embed**".


Rewriting CSS urls
==================

If source CSS contain a relative URL (i.e. relative to current file),
those URL will be converted to full relative path.


Wrapped javascript output
=========================

All javascript output is wrapped in an anonymous function : ::

  (function(){ ... })();

This safety wrapper, make it difficult to pollute the global namespace by accident and improve performance.

You can override this behavior by setting ``PIPELINE_DISABLE_WRAPPER`` to ``True``.
