.. _ref-customization:

=============
Customization
=============

.. note::

  Describes how to customize and add your own functionality to django-compress


django-compress can be customized an a couple of ways.

If you need to change the output of the HTML-tags generated from the templatetags,
this can be done by overriding the templates ``compress/css.html`` and ``compress/js.html``.

You can also write your own compressor-class, if you for example want to implement
other types of compressors.
All you need to do is to define a compress_css and/or a compress_js functions in a
class that inherits from ``compress.compressors.CompressorBase``,
and specify it in the tuple of filters (``COMPRESS_CSS_COMPRESSORS``/``COMPRESS_JS_COMPRESSORS``)
(see :doc:`configuration` for more information) in the settings.

For now, see the files under `compressors/` for more details.