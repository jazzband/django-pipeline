from pipeline.compressors import CompressorBase
from rcssmin import cssmin

class RCSSMinCompressor(CompressorBase):
  def compress_css(self, css):
    return cssmin(css)
