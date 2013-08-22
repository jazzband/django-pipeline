"""
A finder for using Pipeline compressed content with staticfiles
"""

from django.contrib.staticfiles.finders import BaseFinder, find
from django.contrib.staticfiles import finders

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


class CachedFileFinder(BaseFinder):
    """
    A file finder that handles cached file storage
    """

    def find(self, path, all=False):
        """
        Work out the uncached name of the file and look that up instead
        """

        try:
            start, _, extn = path.rsplit('.', 2)
            path = '.'.join((start, extn))

            return find(path, all=all)
        except ValueError:
            return []

    def list(self, *args):
        return []


class BaseContribFinderMixin(object):
    IGNORED_PATTERNS = []

    def list(self, ignore_patterns):
        if ignore_patterns:
            ignore_patterns = ignore_patterns + self.IGNORED_PATTERNS

        return super(BaseContribFinderMixin, self).list(ignore_patterns)


class AppDirectoriesFinder(BaseContribFinderMixin,
                           finders.AppDirectoriesFinder):
    """
    Like AppDirectoriesFinder, but doesn't return any additional ignored
    patterns.

    This allows us to concentrate/compress our components without dragging
    the raw versions in via collectstatic.
    """

    IGNORED_PATTERNS = [
        '*.js',  # we will concentrate it all ourselves through Pipeline
        '*.css',
        '*.less',
        '*.scss',
    ]


class FileSystemFinder(BaseContribFinderMixin, finders.FileSystemFinder):
    """
    Like FileSystemFinder, but doesn't return any additional ignored patterns

    This allows us to concentrate/compress our components without dragging
    the raw versions in too.
    """

    IGNORED_PATTERNS = [
        '*.js',  # we will concentrate it all ourselves through Pipeline
        '*.less',
        '*.scss',
        '*.sh',
        '*.html',
        '*.md',
        '*.markdown',
        '*.php',
        '*.txt',
        'README*',
        'LICENSE*',
        '*examples*',
        '*test*',
        '*bin*',
        '*samples*',
        '*docs*',
        '*build*',
        '*demo*',
        'Makefile*',
        'Gemfile*',
    ]
