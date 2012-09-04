from django.test import TestCase

from pipeline.conf import settings
from pipeline.compilers import Compiler, CompilerBase

from paths import _


class DummyCompiler(CompilerBase):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        return


class CompilerTest(TestCase):
    def setUp(self):
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.compiler.DummyCompiler']

    def test_output_path(self):
        output_path = self.compiler.output_path("js/helpers.coffee", "js")
        self.assertEquals(output_path, "js/helpers.js")

    def test_compilers_class(self):
        compilers_class = self.compiler.compilers
        self.assertEquals(compilers_class[0], DummyCompiler)

    def test_compile(self):
        paths = self.compiler.compile([
            _('pipeline/js/dummy.coffee'),
            _('pipeline/js/application.js'),
        ])
        self.assertEquals([_('pipeline/js/dummy.js'), _('pipeline/js/application.js')], paths)

    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
