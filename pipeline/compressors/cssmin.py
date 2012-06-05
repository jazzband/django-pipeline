from __future__ import absolute_import

from pipeline.compressors import CompressorBase


class CssminCompressor(CompressorBase):
    """
    CSS compressor based on the Python library cssmin
    (http://pypi.python.org/pypi/cssmin/).
    """
    def compress_css(self, css):
        from cssmin import cssmin
        return cssmin(css)
