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

When ``settings.DEBUG`` is set to ``True`` the use of these template tags will
result in a separate tag for each resource in a given group (i.e., the
combined, compressed files will not be used), in order to make local debugging
easy. When ``settings.DEBUG`` is set to ``False`` the opposite is true. You can
override the default behavior by setting ``settings.PIPELINE_ENABLED``
manually. When set to ``True`` or ``False`` this enables or disables,
respectively, the usage of the combined, compressed file for each resource
group. This can be useful, if you encounter errors in your compressed code that
don't occur in your uncompressed code and you want to debug them locally.

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

    $ python manage.py collectstatic

Cache-busting
-------------

Pipeline 1.2+ no longer provides its own cache-busting URL support (using e.g. the ``PIPELINE_VERSIONING`` setting) but uses
Django's built-in staticfiles support for this. To set up cache-busting in conjunction with ``collectstatic`` as above, use ::

    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

This will handle cache-busting just as ``staticfiles``'s built-in ``CachedStaticFilesStorage`` does.

Middleware
==========

To enable HTML compression add ``pipeline.middleware.MinifyHTMLMiddleware``,
to your ``MIDDLEWARE_CLASSES`` settings.

Ensure that it comes after any middleware which modifies your HTML, like ``GZipMiddleware`` ::

   MIDDLEWARE_CLASSES = (
      'django.middleware.gzip.GZipMiddleware',
      'pipeline.middleware.MinifyHTMLMiddleware',
   )

Cache manifest
==============

Pipeline provide a way to add your javascripts and stylesheets files to a
cache-manifest via `Manifesto <http://manifesto.readthedocs.org/>`_.

To do so, you just need to add manifesto app to your ``INSTALLED_APPS``.


Jinja
=====

Pipeline also includes Jinja2 support and is used almost identically to the Django Template tags implementation.
You just need to pass ``pipeline.jinja2.ext.PipelineExtension`` to your Jinja2 environment.

Templates
---------

Unlike the Django template tag implementation the Jinja2 implementation uses different templates, so if you wish to override them please override pipeline/css.jinja and pipeline/js.jinja.
