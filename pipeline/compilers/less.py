from __future__ import unicode_literals

import os

from django.apps import apps
from django.conf import settings as django_settings

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


def _static_paths():
    """Captures all the static direcoties, both from filesystem and apps.

    """
    for path in django_settings.STATICFILES_DIRS:
        yield path
    for app_config in apps.get_app_configs():
        path = os.path.join(app_config.path, 'static')
        if os.path.isdir(path):
            yield path


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        # Pipe to file rather than provide outfile arg due to a bug in lessc
        include_path = '--include-path=%s' % os.pathsep.join(_static_paths())
        command = (
            settings.LESS_BINARY,
            include_path,
            settings.LESS_ARGUMENTS,
            infile,
        )
        return self.execute_command(command, cwd=os.path.dirname(infile), stdout_captured=outfile)
