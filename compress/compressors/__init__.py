import os
import re
import subprocess
import urlparse

from compress.conf import settings
from compress.storage import storage
from compress.utils import to_class

URL_DETECTOR = r'url\([\'"]?([^\s)]+\.[a-z]+)[\'"]?\)'


class Compressor(object):
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

    def compress_css(self, paths):
        """Concatenate and compress CSS files"""
        css = self.concatenate_and_rewrite(paths)
        for compressor in self.css_compressors:
            css = getattr(compressor(verbose=self.verbose), 'compress_css')(css)
        return css

    def concatenate_and_rewrite(self, paths):
        """Concatenate together files and rewrite urls"""
        stylesheets = []
        for path in paths:
            def reconstruct(match):
                asset_path = match.group(1)
                if asset_path.startswith("http") or asset_path.startswith("//"):
                    return "url(%s)" % asset_path
                asset_url = urlparse.urljoin(
                    settings.COMPRESS_URL,
                    self.construct_asset_path(asset_path, path)[1:]
                )
                return "url(%s)" % asset_url
            content = self.read_file(path)
            content = re.sub(URL_DETECTOR, reconstruct, content)
            stylesheets.append(content)
        return '\n'.join(stylesheets)

    def concatenate(self, paths):
        """Concatenate together a list of files"""
        return '\n'.join([self.read_file(path) for path in paths])

    def construct_asset_path(self, asset_path, css_path):
        public_path = self.absolute_path(asset_path, css_path)
        if os.path.isabs(asset_path):
            return asset_path
        else:
            return self.relative_path(public_path)

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
