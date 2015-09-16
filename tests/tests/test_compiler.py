from __future__ import unicode_literals

import os

from django.test import TestCase

from pipeline.conf import settings
from pipeline.compilers import Compiler, CompilerBase, SubProcessCompiler
from pipeline.collector import default_collector
from pipeline.exceptions import CompilerError

from tests.utils import _


class FailingCompiler(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (("/usr/bin/env", "false",),)
        return self.execute_command(command)


class InvalidCompiler(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (
            ("this-exists-nowhere-as-a-command-and-should-fail",),
            infile,
            outfile
        )
        return self.execute_command(command)


class CopyingCompiler(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (
            ("cp",),
            ("--no-dereference", "--preserve=links",),
            infile,
            outfile
        )
        return self.execute_command(command)


class LineNumberingCompiler(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (("/usr/bin/env", "cat"), ("-n",), infile,)
        return self.execute_command(command, stdout_captured=outfile)


class DummyCompiler(CompilerBase):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        return


class DummyCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.test_compiler.DummyCompiler']

    def test_output_path(self):
        output_path = self.compiler.output_path("js/helpers.coffee", "js")
        self.assertEqual(output_path, "js/helpers.js")

    def test_compilers_class(self):
        compilers_class = self.compiler.compilers
        self.assertEqual(compilers_class[0], DummyCompiler)

    def test_compile(self):
        paths = self.compiler.compile([
            _('pipeline/js/dummy.coffee'),
            _('pipeline/js/application.js'),
        ])
        self.assertEqual([_('pipeline/js/dummy.js'), _('pipeline/js/application.js')], list(paths))

    def tearDown(self):
        default_collector.clear()
        settings.PIPELINE_COMPILERS = self.old_compilers

class CompilerStdoutTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.test_compiler.LineNumberingCompiler']

    def test_output_path(self):
        output_path = self.compiler.output_path("js/helpers.coffee", "js")
        self.assertEqual(output_path, "js/helpers.js")

    def test_compile(self):
        paths = self.compiler.compile([_('pipeline/js/dummy.coffee'),])
        self.assertEqual([_('pipeline/js/dummy.junk'),], list(paths))

    def tearDown(self):
        default_collector.clear()
        settings.PIPELINE_COMPILERS = self.old_compilers

class CompilerSelfWriterTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.test_compiler.CopyingCompiler']

    def test_output_path(self):
        output_path = self.compiler.output_path("js/helpers.coffee", "js")
        self.assertEqual(output_path, "js/helpers.js")

    def test_compile(self):
        paths = self.compiler.compile([_('pipeline/js/dummy.coffee'),])
        default_collector.collect()
        self.assertEqual([_('pipeline/js/dummy.junk'),], list(paths))

    def tearDown(self):
        default_collector.clear()
        settings.PIPELINE_COMPILERS = self.old_compilers

class InvalidCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.test_compiler.InvalidCompiler']

    def test_compile(self):
        self.assertRaises(CompilerError,
                self.compiler.compile, [_('pipeline/js/dummy.coffee'),])

    def tearDown(self):
        default_collector.clear()
        settings.PIPELINE_COMPILERS = self.old_compilers

class FailingCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()
        self.old_compilers = settings.PIPELINE_COMPILERS
        settings.PIPELINE_COMPILERS = ['tests.tests.test_compiler.FailingCompiler']

    def test_compile(self):
        self.assertRaises(CompilerError,
                self.compiler.compile, [_('pipeline/js/dummy.coffee'),])

    def tearDown(self):
        default_collector.clear()
        settings.PIPELINE_COMPILERS = self.old_compilers
