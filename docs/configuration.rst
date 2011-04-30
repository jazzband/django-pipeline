.. _ref-configuration:

=============
Configuration
=============


Configuration and list of available settings for django-compress

.. note::
  
  Don't forget to read :doc:`backwardsincompatiblechanges`

Specifying files
================

You specify groups of files to be compressed in your settings.
The basic syntax for specifying CSS/JavaScript groups files is ::

  COMPRESS_CSS = {
      'group_one': {
          'source_filenames': ('css/style.css', 'css/foo.css', 'css/bar.css'),
          'output_filename': 'css/one_compressed.css',
          'extra_context': {
              'media': 'screen,projection',
          },
      },
      # other CSS groups goes here
  }

  COMPRESS_JS = {
      'all': {
          'source_filenames': ('js/jquery-1.2.3.js', 'js/jquery-preload.js', 'js/jquery.pngFix.js',
          'js/my_script.js', 'js/my_other_script.js'),
          'output_filename': 'js/all_compressed.js',
      }
  }

Group options
-------------

* ``source_filenames`` is a tuple with the source files to be compressed.
  The files are concatenated in the order it is specified in the tuple. This option is required.
* ``output_filename`` is the filename of the (to be) compressed file. This option is required.
* ``extra_context`` is a dictionary of values to add to the template context,
  when generating the HTML for the HTML-tags with the templatetags.
  This option is not required and can be left out.
  For CSS, if you do not specify ``extra_context``/``media``, the default media in
  the ``<link>`` output will be ``media="all"``.

Note that all filenames are specified relative to ``COMPRESS_ROOT``, and thus the source
files needs to be in your ``COMPRESS_ROOT``.

Other settings
--------------

* ``COMPRESS``: When ``COMPRESS`` is ``True``, CSS and JavaScripts will be concatenated and filtered.
  When ``False``, the source-files will be used instead.
  Defaults to ``not DEBUG`` (compressed files will only be used in non-DEBUG-mode (production))
* ``COMPRESS_AUTO``: Auto-generate CSS and JavaScript files whenever needed,
  when the template tags are invoked.
  This setting will make sure that the outputted files always are up to date
  (assuming that you are using the provided templatetags to output the links to
  your files).
  If you disable this, you can use the management command to keep your files
  manually updated. Defaults to ``True``.
* ``COMPRESS_VERSION``: Regulates whether or not to add a "version number" to the outputted files filename with for use with “far future Expires”. For more information, see [FarFutureExpires]. When you specify ``COMPRESS_VERSION`` you will also need to add a placeholder (which by default is '?') for the version number in the ``output_filename`` setting.
* ``COMPRESS_VERSION_REMOVE_OLD``: When ``True``, old compressed files will be removed when new versions are generated. All files with a matching name e.g. ``output_filename`` where ? can be replaced by digits will be removed. If you for some reason have files named in the same way, you should consider moving them or putting the compressed files in their own directory. Defaults to ``True``.

``COMPRESS_VERSION`` example::

  COMPRESS = True
  COMPRESS_VERSION = True
  COMPRESS_CSS = {
      'screen': {
          'source_filenames': (
              'css/screen/style.css', 'css/screen/paginator.css',
              'css/screen/agenda.css', 'css/screen/weather.css',
              'css/screen/gallery.css',
          ),
          'output_filename': 'c/screen.r?.css',
      },
  }

This will output a file like ``/media/c/screen.r1213947531.css``, which will be re-generated and updated when you change your source files.

* ``COMPRESS_CSS_COMPRESSORS``: A tuple of filters to be applied to CSS files.
  Defaults to ``('compress.compressors.yui.YUICompressor', )``.
* ``COMPRESS_JS_COMPRESSORS``: A tuple of filters to be applied to JavaScript files.
  Defaults to ``('compress.compressors.yui.YUICompressor',)``

.. note::

  Please note that in order to use YUI Compressor, you need to install YUI Compressor (see :doc:`ìnstallation` for more details).

``COMPRESS_*_COMPRESSORS`` can be set to an empty tuple or None to not use any filters.
The files will however still be concatenated to one file.

Prefix - An Alternative to MEDIA_URL
------------------------------------

In cases where you want to deploy your compiled script and styles to somewhere
other than your MEDIA_URL, say a Content Delivery Network,
you can use the optional ``prefix`` parameter::

  COMPRESS_CSS = {
      'group_one': {
          'source_filenames': ('css/style.css', 'css/foo.css', 'css/bar.css'),
	        'output_filename': 'css/one_compressed.css',
	        'extra_context': {
	            'media': 'screen,projection',
				      'prefix': 'http://cdn.example.com/'
	        },
	    },
	    # other CSS groups goes here
  }

In this example, the template tags will render ``http://cdn.example.com/css/one_compressed.css`` in the link tag.
You will need to manually put there after you build as part of your deployment process.

CSS URL not starting with slash
-------------------------------

If source CSS contain a relative URL not starting with slash (i.e. relative to current file),
those URL will be converted to full relative path using ``COMPRESS_URL``.
This conversion is performed before any filters applied ::

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

(Assuming ``COMPRESS_URL`` is '' or '/', with non-empty ``COMPRESS_URL`` result will be another).


External urls
-------------

While django-compress does a great job of minimizing the amount of http requests
on your site (hence increasing performance) there are sometimes cases when you
want to include external files as well. Let's take an example::

  COMPRESS_JS = {
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

Output in when ``settings.COMPRESS = False``::

  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.5.2/jquery-ui.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="/media/js/blog.js" charset="utf-8"></script><script type="text/javascript" src="/media/js/comments.js" charset="utf-8"></script>

Output in when ``settings.COMPRESS = True``::

  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.5.2/jquery-ui.min.js" charset="utf-8"></script>
  <script type="text/javascript" src="/media/js/all.js" charset="utf-8"></script>

Now why is this good you ask? The more script sources the more impact on performance
according to http://developer.yahoo.com/performance/rules.html#num_http 
which is true but if you are low bandwidth or superbig you may want to offload
some horsepower to google which leads us as hinted in the example above to the next topic.

.. note::
  
  external urls is currently only available for javascript. There's currently no
  reason to have external css files (Yes there are css frameworks as well on the net
  but they are often very small or generated to fit your needs)

Google AJAX Libraries API
-------------------------

So the reason for adding external urls support to django-compress is google ajax
libraries api support (example above) but you may want to use it however you want. 

The advantages for offloading huge javascript libraries to google cdn is of course
that your site will need a lot less bandwidth, even if you use far futures expires headers.
But the superior reason is of course that the more sites that uses it, the bigger
the chance is that your favorite js framework is already cached in your visitors browser. 

Google also uses far future expires headers so don't worry about that.
Don't worry about latency outside the US either. Here in sweden I measured a latency of 39ms.

To sum somethings up, it's up to you and your situation to decide if merging all js
files or offloading js libraries to google gives your site the best performance.
Both ways are great to achieve great performance.

For a complete list of javascript libraries supported go to http://code.google.com/apis/ajaxlibs/

YUI Compressor settings
=======================

* ``COMPRESS_YUI_BINARY``: command line to execute for the YUI program.
  Defaults to ``'java -jar yuicompressor.jar'``. You will most likely change this to the location of yuicompressor on your system.
* ``COMPRESS_YUI_CSS_ARGUMENTS``: Additional arguments to use when compressing CSS.
  Defaults to ``''``.
* ``COMPRESS_YUI_JS_ARGUMENTS``: Additional arguments to use when compressing JavaScript.
  Defaults to ``''``.
