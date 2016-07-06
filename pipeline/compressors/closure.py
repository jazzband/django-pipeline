from __future__ import unicode_literals

import os
import tempfile

from django.contrib.staticfiles.storage import staticfiles_storage

from pipeline.conf import settings
from pipeline.compressors import SubProcessCompressor
from pipeline.utils import source_map_re


class ClosureCompressor(SubProcessCompressor):

    def compress_js(self, js):
        command = (settings.CLOSURE_BINARY, settings.CLOSURE_ARGUMENTS)
        return self.execute_command(command, js)

    def compress_js_with_source_map(self, paths):
        args = [settings.CLOSURE_BINARY, settings.CLOSURE_ARGUMENTS]

        location_maps = set([])

        abs_paths = []
        for path in paths:
            abs_path = staticfiles_storage.path(path)
            location_maps.add("%s|%s" % (
                os.path.dirname(abs_path),
                staticfiles_storage.url(os.path.dirname(path))))
            abs_paths.append(abs_path)
            with open(abs_path) as f:
                content = f.read()
            matches = source_map_re.search(content)
            if matches:
                input_source_map = filter(None, matches.groups())[0]
                input_source_map_file = os.path.join(os.path.dirname(abs_path), input_source_map)
                args += [
                    '--source_map_input',
                    "%s|%s" %  (abs_path, input_source_map_file)]
        for location_map in location_maps:
            args += ['--source_map_location_mapping', location_map]

        temp_file = tempfile.NamedTemporaryFile()

        args += ["--create_source_map", temp_file.name]
        for path in abs_paths:
            args += ["--js", path]

        js = self.execute_command(args, None)

        with open(temp_file.name) as f:
            source_map = f.read()

        temp_file.close()

        return js, source_map
