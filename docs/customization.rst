.. _ref-customization:

=============
Customization
=============

``django-compress`` can be customized an a couple of ways.

If you need to change the output of the HTML-tags generated from the templatetags,
this can be done by overriding the templates ``compress/css.html`` and ``compress/js.html``.

You can also write your own compressor-class, if you for example want to implement
other types of compressors.

All you need to do is to create a class that inherits from ``compress.compressors.CompressorBase``
and implements ``compress_css`` and/or a ``compress_js`` when needed.

Finally, specify it in the tuple of compressors ``COMPRESS_CSS_COMPRESSORS`` or 
``COMPRESS_JS_COMPRESSORS`` (see :doc:`configuration` for more information) in the settings.

Example
=======

A custom compressor for a imaginary compressor called jam ::

  from compress.compressors import CompressorBase
  
  class JamCompressor(CompressorBase):
    def compress_js(self, js):
      return jam.compress(js)
    
    def compress(self, css):
      return jam.compress(css)
  
