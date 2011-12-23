import base64
import os
import re
import subprocess

from itertools import takewhile

from pipeline.conf import settings
from pipeline.storage import storage
from pipeline.utils import filepath_to_uri, to_class, relpath

MAX_IMAGE_SIZE = 32700

EMBEDDABLE = r'[/]?embed/'
URL_DETECTOR = r'url\([\'"]?([^\s)]+\.[a-z]+[\?\#\d\w]*)[\'"]?\)'
URL_REPLACER = r'url\(__EMBED__(.+?)(\?\d+)?\)'

MHTML_START = "/*\r\nContent-Type: multipart/related; boundary=\"MHTML_MARK\"\r\n\r\n"
MHTML_SEPARATOR = "--MHTML_MARK\r\n"
MHTML_END = "\r\n--MHTML_MARK--\r\n*/\r\n"

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

    def js_compressor(self):
        return to_class(settings.PIPELINE_JS_COMPRESSOR)
    js_compressor = property(js_compressor)

    def css_compressor(self):
        return to_class(settings.PIPELINE_CSS_COMPRESSOR)
    css_compressor = property(css_compressor)

    def compress_js(self, paths, templates=None, asset_url=None, **kwargs):
        """Concatenate and compress JS files"""
        js = self.concatenate(paths)
        if templates:
            js = js + self.compile_templates(templates)
        js = "(function() { %s }).call(this);" % js

        compressor = self.js_compressor
        if compressor:
            js = getattr(compressor(verbose=self.verbose), 'compress_js')(js)

        return js

    def compress_css(self, paths, variant=None, asset_url=None,
                     absolute_asset_paths=True, **kwargs):
        """Concatenate and compress CSS files"""
        css = self.concatenate_and_rewrite(paths, variant,
                                           absolute_asset_paths)
        compressor = self.css_compressor
        if compressor:
            css = getattr(compressor(verbose=self.verbose), 'compress_css')(css)
        if not variant:
            return css
        elif variant == "datauri":
            return self.with_data_uri(css)
        elif variant == "mhtml":
            return self.with_mhtml(css, asset_url)
        else:
            raise CompressorError("\"%s\" is not a valid variant" % variant)

    def compile_templates(self, paths):
        compiled = ""
        if not paths:
            return compiled
        namespace = settings.PIPELINE_TEMPLATE_NAMESPACE
        base_path = self.base_path(paths)
        for path in paths:
            contents = self.read_file(path)
            contents = re.sub(r"\r?\n", "", contents)
            contents = re.sub(r"'", "\\'", contents)
            name = self.template_name(path, base_path)
            compiled += "%s['%s'] = %s('%s');\n" % (
                namespace,
                name,
                settings.PIPELINE_TEMPLATE_FUNC,
                contents
            )
        return "\n".join([
            "%(namespace)s = %(namespace)s || {};" % {'namespace': namespace},
            compiled
        ])

    def base_path(self, paths):
        def names_equal(name):
            return all(n == name[0] for n in name[1:])
        directory_levels = zip(*[p.split(os.sep) for p in paths])
        return os.sep.join(x[0] for x in takewhile(names_equal, directory_levels))

    def template_name(self, path, base):
        """Find out the name of a JS template"""
        if not base:
            path = os.path.basename(path)
        if path == base:
            base = os.path.dirname(path)
        name = re.sub(r"^%s[\/\\]?(.*)%s$" % (
            re.escape(base), re.escape(settings.PIPELINE_TEMPLATE_EXT)
        ), r"\1", path)
        return re.sub(r"[\/\\]", "_", name)

    def concatenate_and_rewrite(self, paths, variant=None, absolute_asset_paths=True):
        """Concatenate together files and rewrite urls"""
        stylesheets = []
        for path in paths:
            def reconstruct(match):
                asset_path = match.group(1)
                if asset_path.startswith("http") or asset_path.startswith("//"):
                    return "url(%s)" % asset_path
                asset_url = self.construct_asset_path(asset_path, path,
                    variant, absolute_asset_paths)
                return "url(%s)" % asset_url
            content = self.read_file(path)
            content = re.sub(URL_DETECTOR, reconstruct, content)
            stylesheets.append(content)
        return '\n'.join(stylesheets)

    def concatenate(self, paths):
        """Concatenate together a list of files"""
        return '\n'.join([self.read_file(path) for path in paths])

    def construct_asset_path(self, asset_path, css_path, variant=None, absolute_asset_paths=True):
        """Return a rewritten asset URL for a stylesheet"""
        public_path = self.absolute_path(asset_path, os.path.dirname(css_path))
        if self.embeddable(public_path, variant):
            return "__EMBED__%s" % public_path
        if not absolute_asset_paths:
            return asset_path
        if not os.path.isabs(asset_path):
            asset_path = self.relative_path(public_path)
        asset_url = filepath_to_uri(asset_path)
        return settings.PIPELINE_URL + asset_url[1:]

    def embeddable(self, path, variant):
        """Is the asset embeddable ?"""
        name, ext = os.path.splitext(path)
        font = ext in FONT_EXTS
        if not variant:
            return False
        if not (re.search(EMBEDDABLE, path) and storage.exists(path)):
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

    def with_mhtml(self, css, asset_url):
        paths = {}
        def mhtml(match):
            path = match.group(1)
            if not path in paths:
                paths[path] = "%s-%s" % (match.start(), os.path.basename(path))
            return "url(mhtml:%s!%s)" % (asset_url, paths[path])
        css = re.sub(URL_REPLACER, mhtml, css)
        mhtml = []
        for path, location in paths.items():
            mime_type = self.mime_type(path)
            data = self.encoded_content(path)
            mhtml.extend([
                MHTML_SEPARATOR,
                "Content-Location: %s\r\n" % location,
                "Content-Type: %s\r\n" % mime_type,
                "Content-Transfer-Encoding: base64\r\n\r\n",
                data,
                "\r\n"
            ])
        output = [MHTML_START, mhtml, MHTML_END, css]
        return ''.join([part for parts in output for part in parts])

    def encoded_content(self, path):
        """Return the base64 encoded contents"""
        if path in self.__class__.asset_contents:
            return self.__class__.asset_contents[path]
        data = self.read_file(path)
        self.__class__.asset_contents[path] = base64.b64encode(data)
        return self.__class__.asset_contents[path]

    def mime_type(self, path):
        """Get mime-type from filename"""
        name, ext = os.path.splitext(path)
        return MIME_TYPES[ext]

    def absolute_path(self, path, start):
        """
        Return the absolute public path for an asset,
        given the path of the stylesheet that contains it.
        """
        if os.path.isabs(path):
            path = os.path.join(settings.PIPELINE_ROOT, path)
        else:
            path = os.path.join(start, path)
        return os.path.normpath(path)

    def relative_path(self, absolute_path):
        """Rewrite paths relative to the output stylesheet path"""
        absolute_path = self.absolute_path(absolute_path, settings.PIPELINE_ROOT)
        return os.path.join(os.sep, relpath(absolute_path, settings.PIPELINE_ROOT))

    def read_file(self, path):
        """Read file content in binary mode"""
        file = storage.open(path, 'rb')
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
