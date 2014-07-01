from pipeline.compressors import Compressor, CompressorBase

class NoOpCompressor(CompressorBase):
    def compress_js(self, js):
        return js

    def compress_css(self, css):
        return css
