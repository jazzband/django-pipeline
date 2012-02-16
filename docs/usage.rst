.. _ref-usage:

=====
Usage
=====

Describes how to use Pipeline when it is installed and configured.

Templatetags
============

Pipeline includes two template tags: ``compressed_css`` and ``compressed_js``,
in a template library called ``compressed``.

They are used to output the ``<link>`` and ``<script>``-tags for the
specified CSS/JavaScript-groups (as specified in the settings).
The first argument must be the name of the CSS/JavaScript group.

The templatetags will either output the source filenames or the compressed filenames,
depending on the ``PIPELINE`` setting, if you do not specify the ``PIPELINE`` setting,
the source files will be used in DEBUG-mode, and compressed files in non-DEBUG-mode.

If you need to change the output of the HTML-tags generated from the templatetags,
this can be done by overriding the templates ``pipeline/css.html`` and ``pipeline/js.html``.

Example
-------

If you have specified the CSS-groups “screen” and “print” and a JavaScript-group
with the name “scripts”, you would use the following code to output them all ::

   {% load compressed %}
   {% compressed_css 'colors' %}
   {% compressed_js 'stats' %}


Collect static
==============

Pipeline integrates with staticfiles, you just need to setup ``STATICFILES_STORAGE`` to ::

    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
    
Then when you run ``collectstatic`` command, your CSS and your javascripts will be compressed in the same time ::

    $ python oslo/manage.py collectstatic


Middleware
==========

To enable HTML compression add ``pipeline.middleware.MinifyHTMLMiddleware``, 
to your ``MIDDLEWARE_CLASSES`` settings.

Ensure that it comes after any middleware which modify your HTML, like ``GZipMiddleware`` ::

   MIDDLEWARE_CLASSES = (
      'django.middleware.gzip.GZipMiddleware',
      'pipeline.middleware.MinifyHTMLMiddleware',
   )

Cache manifest
==============

Pipeline provide a way to add your javascripts and stylesheets files to a
cache-manifest via `Manifesto <http://manifesto.readthedocs.org/>`_.

To do so, you just need to add manifesto app to your ``INSTALLED_APPS``.
