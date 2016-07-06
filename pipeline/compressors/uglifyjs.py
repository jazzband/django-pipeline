from __future__ import unicode_literals

import codecs
import tempfile

from django.contrib.staticfiles.storage import staticfiles_storage

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor
from pipeline.utils import source_map_re, path_depth


class UglifyJSCompressor(SubProcessCompressor):

    def compress_js(self, js):
        command = [settings.UGLIFYJS_BINARY, settings.UGLIFYJS_ARGUMENTS]
        if self.verbose:
            command.append(' --verbose')
        return self.execute_command(command, js)

    def compress_js_with_source_map(self, paths):
        source_map_file = tempfile.NamedTemporaryFile()

        args = [settings.UGLIFYJS_BINARY]
        args += [staticfiles_storage.path(p) for p in paths]
        args += ["--source-map", source_map_file.name]
        args += ["--source-map-root", staticfiles_storage.base_url]
        args += ["--prefix", "%s" % path_depth(staticfiles_storage.base_location)]

        args += settings.UGLIFYJS_ARGUMENTS

        if self.verbose:
            args.append('--verbose')

        js = self.execute_command(args)

        with codecs.open(source_map_file.name, encoding='utf-8') as f:
            source_map = f.read()

        source_map_file.close()

        # Strip out existing source map comment (it will be re-added with packaging)
        js = source_map_re.sub('', js)

        return js, source_map
