from compress.utils import media_root
from compress.compressors.jsmin.jsmin import jsmin

class JSMinCompressor:
    def compress_css(self, css):
        raise NotImplementedError

    def compress_js(self, js):
        source = ''
        for source_filename in js['source_filenames']:
            fd = open(media_root(source_filename), 'r')
            source += fd.read()
            source += ';'
            fd.close()
        
        compressed = jsmin(source)
        fd = open(media_root(js['compressed_filename']), 'w+')
        fd.write(compressed)
        fd.close()