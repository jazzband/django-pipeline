from pipeline.compressors import CompressorBase
from pipeline.compressors.jsmin.jsmin import jsmin


class JSMinCompressor(CompressorBase):
    def compress_js(self, js):
        return jsmin(js)
