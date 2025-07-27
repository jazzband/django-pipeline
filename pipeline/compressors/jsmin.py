from pipeline.compressors import CompressorBase


class JSMinCompressor(CompressorBase):
    """
    JS compressor based on the Python library jsmin
    (http://pypi.python.org/pypi/jsmin/).
    """

    def compress_js(self, js):
        from jsmin import jsmin  # noqa: PLC0415

        return jsmin(js)
