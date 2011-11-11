import os

from django.template import Context
from django.test import TestCase

from pipeline.conf import settings
from pipeline.compilers import CompilerBase
from pipeline.templatetags.compressed import CompressedCSSNode


class DummyCompiler(CompilerBase):
    uncompiled_css_rel = 'stylesheet/mycss'
    output_extension = 'css'

    def match_file(self, path):
        return path.endswith('.mycss')

    def compile_file(self, content, path):
        return content


class TemplateTagsTest(TestCase):
    def setUp(self):
        self.old_compilers = settings.PIPELINE_COMPILERS
        self.old_pipeline = settings.PIPELINE
        self.old_pipeline_auto = settings.PIPELINE_AUTO
        self.old_pipeline_css = settings.PIPELINE_CSS
        self.old_pipeline_css_compressor = settings.PIPELINE_CSS_COMPRESSOR

        settings.PIPELINE_COMPILERS = ['tests.tests.templatetags.DummyCompiler']
        settings.PIPELINE_CSS_COMPRESSOR = None

    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
        settings.PIPELINE = self.old_pipeline
        settings.PIPELINE_AUTO = self.old_pipeline_auto
        settings.PIPELINE_CSS = self.old_pipeline_css
        settings.PIPELINE_CSS_COMPRESSOR = self.old_pipeline_css_compressor

        reltest = os.path.join(settings.PIPELINE_ROOT, 'css', 'reltest.css')

        if os.path.exists(reltest):
            os.unlink(reltest)

    def test_render_css(self):
        settings.PIPELINE_CSS = {
            'test': {
                'source_filenames': ('css/reltest.mycss',),
                'output_filename': 'css/reltest.css',
            }
        }

        node = CompressedCSSNode('"test"')

        settings.PIPELINE = True
        settings.PIPELINE_AUTO = True
        self.assertTrue('rel="stylesheet"' in node.render(Context({})))

        settings.PIPELINE = False
        settings.PIPELINE_AUTO = False
        self.assertTrue('rel="stylesheet/mycss"' in node.render(Context({})))
