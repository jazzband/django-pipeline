from __future__ import unicode_literals

import sys
from unittest import skipIf, skipUnless

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.encoding import smart_bytes

from pipeline.collector import default_collector
from pipeline.compilers import Compiler, CompilerBase, SubProcessCompiler
from pipeline.exceptions import CompilerError
from pipeline.utils import to_class

from tests.utils import _, pipeline_settings


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

class CompilerWithEmptyFirstArg(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (
            ('', '/usr/bin/env', 'cat'),
            infile,
        )
        return self.execute_command(command, stdout_captured=outfile)

class CopyingCompiler(SubProcessCompiler):
    output_extension = 'junk'

    def match_file(self, path):
        return path.endswith('.coffee')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = (
            "cp",
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


@pipeline_settings(COMPILERS=['tests.tests.test_compiler.DummyCompiler'])
class DummyCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_output_path(self):
        compiler_class = self.compiler.compilers[0]
        compiler = compiler_class(verbose=self.compiler.verbose, storage=self.compiler.storage)
        output_path = compiler.output_path("js/helpers.coffee", "js")
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


@skipIf(sys.platform.startswith("win"), "requires posix platform")
@pipeline_settings(COMPILERS=['tests.tests.test_compiler.LineNumberingCompiler'])
class CompilerStdoutTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_output_path(self):
        compiler_class = self.compiler.compilers[0]
        compiler = compiler_class(verbose=self.compiler.verbose, storage=self.compiler.storage)
        output_path = compiler.output_path("js/helpers.coffee", "js")
        self.assertEqual(output_path, "js/helpers.js")

    def test_compile(self):
        paths = self.compiler.compile([_('pipeline/js/dummy.coffee')])
        self.assertEqual([_('pipeline/js/dummy.junk')], list(paths))

    def tearDown(self):
        default_collector.clear()


@skipIf(sys.platform.startswith("win"), "requires posix platform")
@pipeline_settings(COMPILERS=['tests.tests.test_compiler.CopyingCompiler'])
class CompilerSelfWriterTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_output_path(self):
        compiler_class = self.compiler.compilers[0]
        compiler = compiler_class(verbose=self.compiler.verbose, storage=self.compiler.storage)
        output_path = compiler.output_path("js/helpers.coffee", "js")
        self.assertEqual(output_path, "js/helpers.js")

    def test_compile(self):
        paths = self.compiler.compile([_('pipeline/js/dummy.coffee')])
        default_collector.collect()
        self.assertEqual([_('pipeline/js/dummy.junk')], list(paths))

    def tearDown(self):
        default_collector.clear()


@pipeline_settings(COMPILERS=['tests.tests.test_compiler.CompilerWithEmptyFirstArg'])
class CompilerWithEmptyFirstArgTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_compile(self):
            paths = self.compiler.compile([_('pipeline/js/dummy.coffee')])
            default_collector.collect()
            self.assertEqual([_('pipeline/js/dummy.junk')], list(paths))

    def tearDown(self):
        default_collector.clear()

@pipeline_settings(COMPILERS=['tests.tests.test_compiler.InvalidCompiler'])
class InvalidCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_compile(self):
        with self.assertRaises(CompilerError) as cm:
            self.compiler.compile([_('pipeline/js/dummy.coffee')])
            e = cm.exception
            self.assertEqual(
                e.command,
                ['this-exists-nowhere-as-a-command-and-should-fail',
                 'pipeline/js/dummy.coffee',
                 'pipeline/js/dummy.junk'])
            self.assertEqual(e.error_output, '')

    def tearDown(self):
        default_collector.clear()


@skipIf(sys.platform.startswith("win"), "requires posix platform")
@pipeline_settings(COMPILERS=['tests.tests.test_compiler.FailingCompiler'])
class FailingCompilerTest(TestCase):
    def setUp(self):
        default_collector.collect()
        self.compiler = Compiler()

    def test_compile(self):
        with self.assertRaises(CompilerError) as cm:
            self.compiler.compile([_('pipeline/js/dummy.coffee')])

            e = cm.exception
            self.assertEqual(e.command, ['/usr/bin/env', 'false'])
            self.assertEqual(e.error_output, '')

    def tearDown(self):
        default_collector.clear()


@skipUnless(settings.HAS_NODE, "requires node")
class CompilerImplementation(TestCase):

    def setUp(self):
        self.compiler = Compiler()
        default_collector.collect(RequestFactory().get('/'))

    def tearDown(self):
        default_collector.clear()

    def _test_compiler(self, compiler_cls_str, infile, expected):
        compiler_cls = to_class(compiler_cls_str)
        compiler = compiler_cls(verbose=False, storage=staticfiles_storage)
        infile_path = staticfiles_storage.path(infile)
        outfile_path = compiler.output_path(infile_path, compiler.output_extension)
        compiler.compile_file(_(infile_path), _(outfile_path), force=True)
        with open(outfile_path) as f:
            result = f.read()
        with staticfiles_storage.open(expected) as f:
            expected = f.read()
        self.assertEqual(smart_bytes(result), expected)

    def test_sass(self):
        self._test_compiler('pipeline.compilers.sass.SASSCompiler',
            'pipeline/compilers/scss/input.scss',
            'pipeline/compilers/scss/expected.css')

    def test_coffeescript(self):
        self._test_compiler('pipeline.compilers.coffee.CoffeeScriptCompiler',
            'pipeline/compilers/coffee/input.coffee',
            'pipeline/compilers/coffee/expected.js')

    def test_less(self):
        self._test_compiler('pipeline.compilers.less.LessCompiler',
            'pipeline/compilers/less/input.less',
            'pipeline/compilers/less/expected.css')

    def test_es6(self):
        self._test_compiler('pipeline.compilers.es6.ES6Compiler',
            'pipeline/compilers/es6/input.es6',
            'pipeline/compilers/es6/expected.js')

    def test_stylus(self):
        self._test_compiler('pipeline.compilers.stylus.StylusCompiler',
            'pipeline/compilers/stylus/input.styl',
            'pipeline/compilers/stylus/expected.css')

    def test_livescript(self):
        self._test_compiler('pipeline.compilers.livescript.LiveScriptCompiler',
            'pipeline/compilers/livescript/input.ls',
            'pipeline/compilers/livescript/expected.js')
