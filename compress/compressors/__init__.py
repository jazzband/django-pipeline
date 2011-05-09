import base64
import os
import re
import subprocess
import urlparse

from compress.conf import settings
from compress.storage import storage
from compress.utils import to_class

MAX_IMAGE_SIZE = 32700

EMBEDDABLE = r'[\A\/]embed\/'
URL_DETECTOR = r'url\([\'"]?([^\s)]+\.[a-z]+)[\'"]?\)'
URL_REPLACER = r'url\(__EMBED__(.+?)(\?\d+)?\)'

MIME_TYPES = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.ttf': 'font/truetype',
    '.otf': 'font/opentype',
    '.woff': 'font/woff'
}
EMBED_EXTS = MIME_TYPES.keys()
FONT_EXTS = ['.ttf', '.otf', '.woff']


class Compressor(object):
    asset_contents = {}

    def __init__(self, verbose=False):
        self.verbose = verbose

    def js_compressors(self):
        return [to_class(compressor) for compressor in settings.COMPRESS_JS_COMPRESSORS]
    js_compressors = property(js_compressors)

    def css_compressors(self):
        return [to_class(compressor) for compressor in settings.COMPRESS_CSS_COMPRESSORS]
    css_compressors = property(css_compressors)

    def compress_js(self, paths):
        """Concatenate and compress JS files"""
        js = self.concatenate(paths)
        for compressor in self.js_compressors:
            js = getattr(compressor(verbose=self.verbose), 'compress_js')(js)
        return js

    def compress_css(self, paths, variant=None):
        """Concatenate and compress CSS files"""
        css = self.concatenate_and_rewrite(paths, variant)
        for compressor in self.css_compressors:
            css = getattr(compressor(verbose=self.verbose), 'compress_css')(css)
        if not variant:
            return css
        elif variant == "datauri":
            return self.with_data_uri(css)
        else:
            raise CompressorError("\"%s\" is not a valid variant" % variant)

    def concatenate_and_rewrite(self, paths, variant=None):
        """Concatenate together files and rewrite urls"""
        stylesheets = []
        for path in paths:
            def reconstruct(match):
                asset_path = match.group(1)
                if asset_path.startswith("http") or asset_path.startswith("//"):
                    return "url(%s)" % asset_path
                asset_url = self.construct_asset_path(asset_path, path, variant)
                return "url(%s)" % asset_url
            content = self.read_file(path)
            content = re.sub(URL_DETECTOR, reconstruct, content)
            stylesheets.append(content)
        return '\n'.join(stylesheets)

    def concatenate(self, paths):
        """Concatenate together a list of files"""
        content = '\n'.join([self.read_file(path) for path in paths])
        return "(function() { %s }).call(this);" % content

    def construct_asset_path(self, asset_path, css_path, variant=None):
        public_path = self.absolute_path(asset_path, css_path)
        if self.embeddable(public_path, variant):
            return "__EMBED__%s" % public_path
        if not os.path.isabs(asset_path):
            asset_path = self.relative_path(public_path)
        return urlparse.urljoin(settings.COMPRESS_URL, asset_path[1:])

    def embeddable(self, path, variant):
        name, ext = os.path.splitext(path)
        font = ext in FONT_EXTS
        if not variant:
            return False
        if not re.match(path, EMBEDDABLE) and not os.path.exists(path):
            return False
        if not ext in EMBED_EXTS:
            return False
        if not (font or len(self.encoded_content(path)) < MAX_IMAGE_SIZE):
            return False
        return True

    def with_data_uri(self, css):
        def datauri(match):
            path = match.group(1)
            mime_type = self.mime_type(path)
            data = self.encoded_content(path)
            return "url(\"data:%s;charset=utf-8;base64,%s\")" % (mime_type, data)
        return re.sub(URL_REPLACER, datauri, css)

    def encoded_content(self, path):
        if path in self.__class__.asset_contents:
            return self.__class__.asset_contents[path]
        data = self.read_file(path)
        self.__class__.asset_contents[path] = base64.b64encode(data)
        return self.__class__.asset_contents[path]

    def mime_type(self, path):
        name, ext = os.path.splitext(path)
        return MIME_TYPES[ext]

    def absolute_path(self, asset_path, css_path):
        if os.path.isabs(asset_path):
            path = os.path.join(settings.COMPRESS_ROOT, asset_path)
        else:
            path = os.path.join(os.path.dirname(css_path), asset_path)
        return os.path.normpath(path)

    def relative_path(self, absolute_path):
        compress_root = os.path.normpath(settings.COMPRESS_ROOT)
        return os.path.join('../', absolute_path.replace(compress_root, ''))

    def read_file(self, path):
        """Read file content in binary mode"""
        file = storage.open(path, mode='rb')
        content = file.read()
        file.close()
        return content


class CompressorBase(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def filter_css(self, css):
        raise NotImplementedError

    def filter_js(self, js):
        raise NotImplementedError


class CompressorError(Exception):
    """This exception is raised when a filter fails"""
    pass


class SubProcessCompressor(CompressorBase):
    def execute_command(self, command, content):
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        pipe.stdin.write(content)
        pipe.stdin.close()

        compressed_content = pipe.stdout.read()
        pipe.stdout.close()

        error = pipe.stderr.read()
        pipe.stderr.close()

        if pipe.wait() != 0:
            if not error:
                error = "Unable to apply %s compressor" % self.__class__.__name__
            raise CompressorError(error)

        if self.verbose:
            print error

        return compressed_content
