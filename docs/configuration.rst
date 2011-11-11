.. _ref-configuration:

=============
Configuration
=============


Configuration and list of available settings for Pipeline

.. note::
  
  If you are updating from django-compress or from previous versions of django-pipeline,
  don't forget to read :doc:`changelog`.

Specifying files
================

You specify groups of files to be compressed in your settings. You can use glob 
syntax to select multiples files.

The basic syntax for specifying CSS/JavaScript groups files is ::

  PIPELINE_CSS = {
      'group_one': {
          'source_filenames': (
            'css/style.css',
            'css/foo.css',
            'css/button/*.css',
            'css/bar.css'
          ),
          'output_filename': 'css/one_compressed.css',
          'extra_context': {
              'media': 'screen,projection',
          },
      },
      # other CSS groups goes here
  }

  PIPELINE_JS = {
      'all': {
          'source_filenames': (
            'js/jquery-1.2.3.js',
            'js/jquery-preload.js',
            'js/jquery.pngFix.js',
            'js/my_script.js',
            'js/my_other_script.js'
          ),
          'output_filename': 'js/all_compressed.js',
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
  and fonts in CSS with data-URI or MHTML.
  Allowed values are : ``None``, ``datauri`` or ``mhtml``.
  
  Defaults to ``None``.


``manifest``
............

  **Optional**

  Indicate if you want this group to appear in your cache manifest.

  Defaults to ``True``.

``extra_context``
.................

  **Optional**
  
  Is a dictionary of values to add to the template context,
  when generating the HTML for the HTML-tags with the templatetags.
  
  For CSS, if you do not specify ``extra_context``/``media``, the default media in
  the ``<link>`` output will be ``media="all"``.

``absolute_asset_paths``
........................

  **Optional**

  Indicates if relative paths in CSS files should be made absolute, based on
  ``PIPELINE_URL``. This only applies to entries in ``PIPELINE_CSS``.

  Defaults to ``True``.

.. note::

  Note that all filenames are specified relative to ``PIPELINE_ROOT``, and thus the source
  files needs to be in your ``PIPELINE_ROOT``.

Other settings
--------------

``PIPELINE``
............

  When ``PIPELINE`` is ``True``, CSS and JavaScripts will be concatenated and filtered.
  When ``False``, the source-files will be used instead.

  Defaults to ``not DEBUG`` (compressed files will only be used when ``DEBUG`` is ``False``).

``PIPELINE_AUTO``
.................

  Auto-generate CSS and JavaScript files whenever needed, when the template tags
  are invoked.
  
  This setting will make sure that the outputted files always are up to date
  (assuming that you are using the provided templatetags to output the links to
  your files).
  
  If you disable this, you can use the management command to keep your files
  manually updated.
  
  Defaults to ``True``.

``PIPELINE_VERSION``
....................

  Regulates whether or not to add a "version number" to the outputted files
  filename with for use with “far future Expires”.
  
  When you specify ``PIPELINE_VERSION`` you will also need to add a placeholder
  (which by default is ``?``) for the version number in the ``output_filename`` setting.

``PIPELINE_VERSION_REMOVE_OLD``
...............................

  When ``True``, old compressed files will be removed when new versions are generated.
  All files with a matching name e.g. ``output_filename`` where ``?`` can be replaced
  by digits will be removed.
  
  If you for some reason have files named in the same way, you should consider moving
  them or putting the compressed files in their own directory. 
  
  Defaults to ``True``.

  Example::

    PIPELINE = True
    PIPELINE_VERSION = True
    PIPELINE_CSS = {
        'screen': {
            'source_filenames': (
                'css/screen/style.css', 'css/screen/paginator.css',
                'css/screen/agenda.css', 'css/screen/weather.css',
                'css/screen/gallery.css',
            ),
            'output_filename': 'c/screen.r?.css',
        },
    }

  This will output a file like ``/media/c/screen.r1213947531.css``,
  which will be re-generated and updated when you change your source files.

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

``PIPELINE_CACHE_TIMEOUT``
..........................

  Package version are cached to avoid unnecessary IO, the default is to cache
  version for 2 years.

  Defaults to ``63072000``

Embedding fonts and images
==========================

You can embed fonts and images directly in your compiled css, using Data-URI in 
modern browser or MHTML in Internet Explorer 7 or below. 

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
and ``absolute_asset_paths`` is set to ``True`` or left out in the package
entry, the URL will be converted to full relative path using ``PIPELINE_URL``.
This conversion is performed before any compressors are applied ::

  media/js/fancybox/
    fancybox.png
    fancybox-x.png
    fancybox-y.png
    jquery.fancybox-1.3.4.css
    jquery.fancybox-1.3.4.js

jquery.fancybox-1.3.4.css contains ::

  background-image: url('fancybox.png');
  background-image: url('fancybox-x.png');
  background-image: url('fancybox-y.png');


In resulting CSS it will be rewritten to ::

  background-image:url(/js/fancybox/fancybox.png);
  background-image:url(/js/fancybox/fancybox-x.png);
  background-image:url(/js/fancybox/fancybox-y.png);

(Assuming ``PIPELINE_URL`` is '' or '/', with non-empty ``PIPELINE_URL`` result will be another).


External urls
=============

.. warning::

    This feature is currently deprecated and will be remove in next major version of pipeline.

While Pipeline does a great job of minimizing the amount of http requests
on your site (hence increasing performance) there are sometimes cases when you
want to include external files as well. Let's take an example::

  PIPELINE_JS = {
      'jquery': {
          'external_urls': (
              'http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.5.2/jquery-ui.min.js'
          ),
      },
      'all': {
          'source_filenames': ('js/blog.js', 'js/comments.js'),
          'output_filename': 'js/all.js',
      },
  }

In template::

    {% load compressed %}
    {% compressed_js 'jquery' %}
    {% compressed_js 'all' %}

Output in when ``settings.PIPELINE = False``::

  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.5.2/jquery-ui.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="/media/js/blog.js" charset="utf-8"></script>
  <script type="text/javascript" src="/media/js/comments.js" charset="utf-8"></script>

Output in when ``settings.PIPELINE = True``::

  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.5.2/jquery-ui.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="/media/js/all.js" charset="utf-8"></script>

Now why is this good you ask? The more script sources the more impact on performance
according to http://developer.yahoo.com/performance/rules.html#num_http 
which is true but if you are low bandwidth or superbig you may want to offload
some horsepower to google which leads us as hinted in the example above to the next topic.

.. note::
  
  External urls is currently only available for javascript.
