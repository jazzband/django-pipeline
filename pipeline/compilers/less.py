from __future__ import unicode_literals

from os.path import dirname
from django.contrib.staticfiles.finders import get_finders

from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler


class LessCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.less')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = '%s %s %s %s --include-path="%s"' % (
            settings.PIPELINE_LESS_BINARY,
            settings.PIPELINE_LESS_ARGUMENTS,
            infile,
            outfile,
            ':'.join(self.get_all_static_dirs())
        )
        return self.execute_command(command, cwd=dirname(infile))

    def get_all_static_dirs(self):
        """
        Get a list of all static file dirs which can be searched as
        defined in ``django.conf.settings.STATICFILES_FINDERS``.

        This is helpful for a less compiler if there are imports within
        less files which reference other static files in different
        Django apps. By providing the compiler a list of folders it
        should consider, it allows it to resolve the import paths.
        """
        dirs = set()

        for finder in get_finders():
            if hasattr(finder, 'storage'):
                storages = [finder.storage]
            elif hasattr(finder, 'storages'):
                storages = finder.storages.values()
            else:
                continue

            for storage in storages:
                if not hasattr(storage, 'location'):
                    continue

                dirs.add(dirname(storage.location))

        return list(dirs)
