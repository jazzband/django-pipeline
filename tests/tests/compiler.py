from django.test import TestCase

from pipeline.compilers import Compiler


class CompilerTest(TestCase):
    def setUp(self):
        self.compiler = Compiler()

    def test_output_path(self):
        output_path = self.compiler.output_path("js/helpers.coffee", "js")
        self.assertEquals(output_path, "js/helpers.js")
