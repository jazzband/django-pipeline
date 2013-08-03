"""
A finder for using Pipeline compressed content with staticfiles
"""

from django.contrib.staticfiles.finders import BaseFinder

from django.utils._os import safe_join

from pipeline.conf import settings


class PipelineFinder(BaseFinder):
    """
    A file finder for Pipeline created assets
    """

    def find(self, path, all=False):
        """
        Looks for files in PIPELINE_CSS and PIPELINE_JS
        """

        matches = []

        for elem in settings.PIPELINE_CSS.values() + \
                    settings.PIPELINE_JS.values():
            if elem['output_filename'] == path:
                match = safe_join(settings.PIPELINE_ROOT, path)
                if not all:
                    return match
                matches.append(match)

        return matches

    def list(self, *args):
        return []
