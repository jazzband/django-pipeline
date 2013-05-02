from __future__ import absolute_import, unicode_literals

from pipeline.compressors import CompressorBase


class RCSSminCompressor(CompressorBase):
    '''
    CSS compressor based on RCSSmin, a full python CSS compressor.

    See `rCSSmin official page <http://opensource.perlig.de/rcssmin/>`_
    '''
    def compress_css(self, css):
        from rcssmin import cssmin
        return cssmin(css)
