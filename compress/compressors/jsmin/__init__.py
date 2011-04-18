from compress.compressors import CompressorBase
from compress.compressors.jsmin.jsmin import jsmin


class JSMinCompressor(CompressorBase):
    def compress_js(self, js):
        return jsmin(js)
