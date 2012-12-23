try:
    from staticfiles.storage import staticfiles_storage
except ImportError:
    from django.contrib.staticfiles.storage import staticfiles_storage  # noqa

from jinja2.ext import Extension


class PipelineExtension(Extension):
    tags = set(['compressed_css', 'compressed_js'])

    def parse(self, parser):
        return []
