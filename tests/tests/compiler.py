from datetime import datetime
from time import time
from os import utime

from django.test import TestCase

from pipeline.conf import settings
from pipeline.compilers import Compiler, CompilerBase
from pipeline.storage import PipelineFinderStorage

from pipeline.compilers.common_css import get_by_name
from pipeline.compilers.less import LessFileTree, LessCompiler
from pipeline.compilers.stylus import StylusFileTree, StylusCompiler
from pipeline.compilers.sass import SASSFileTree, SASSCompiler

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
        self.assertEquals(
            [_('pipeline/js/dummy.js'), _('pipeline/js/application.js')],
            paths
        )

    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers


class FileTreeTestBase(object):
    def setUp(self):
        self.storage = PipelineFinderStorage()

    def test_flatlist(self):
        tree = get_by_name(self.actual_class, self.storage, self.infile)

        flat = tree.flatlist(datetime.fromtimestamp(0))

        files = []
        for node in flat:
            files.append(node.name)
        files.sort()

        self.assertEquals(files, self.flatlist)


class LessFileTreeTest(FileTreeTestBase, TestCase):
    infile = 'pipeline/less/a.less'
    flatlist = [
        'pipeline/less/a.less',
        'pipeline/less/b.less',
        'pipeline/less/c.less'
    ]
    actual_class = LessFileTree


class StylusFileTreeTest(FileTreeTestBase, TestCase):
    infile = 'pipeline/stylus/a.styl'
    flatlist = [
        'pipeline/stylus/a.styl',
        'pipeline/stylus/b.styl',
        'pipeline/stylus/c.styl'
    ]
    actual_class = StylusFileTree


class SASSFileTreeTest(FileTreeTestBase, TestCase):
    infile = 'pipeline/sass/a.scss'
    flatlist = [
        'pipeline/sass/a.scss',
        'pipeline/sass/b.sass',
        'pipeline/sass/c.sass'
    ]
    actual_class = SASSFileTree


class CssCompilerTestBase(object):
    actual_class = None
    root_file = None
    update_file = None

    def setUp(self):
        self.storage = PipelineFinderStorage()
        self.compiler = self.actual_class(False, self.storage)
        self.tmp_name = self.root_file + "-tmp"

        open(self.storage.path(self.root_file) + '-tmp', 'w').close()

    def test_is_outdated(self):
        real_update_file = self.storage.path(self.update_file)
        real_tmp_file = self.storage.path(self.tmp_name)

        # First round, shoud be outdated
        utime(real_tmp_file, (0, 0))
        self.assertEquals(
            True,
            self.compiler.is_outdated(self.root_file, self.tmp_name)
        )

        # Second round, should not be outdated
        utime(real_tmp_file, None)
        self.assertEquals(
            False,
            self.compiler.is_outdated(self.root_file, self.tmp_name)
        )

        # Third and final round, a source file is changed, should be outdated
        utime(real_update_file, (
            time() + 1,
            time() + 1
        ))
        self.assertEquals(
            True,
            self.compiler.is_outdated(self.root_file, self.tmp_name)
        )

    def tearDown(self):
        self.storage.delete(self.tmp_name)


class LessCompilerTest(CssCompilerTestBase, TestCase):
    actual_class = LessCompiler
    root_file = 'pipeline/less/a.less'
    update_file = 'pipeline/less/c.less'


class StylusCompilerTest(CssCompilerTestBase, TestCase):
    actual_class = StylusCompiler
    root_file = 'pipeline/stylus/a.styl'
    update_file = 'pipeline/stylus/c.styl'


class SASSCompilerTest(CssCompilerTestBase, TestCase):
    actual_class = SASSCompiler
    root_file = 'pipeline/sass/a.scss'
    update_file = 'pipeline/sass/c.sass'
