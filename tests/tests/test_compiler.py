from __future__ import unicode_literals

from django.test import TestCase
from mock import MagicMock, patch

from pipeline.conf import settings
from pipeline.compilers import Compiler, CompilerBase

from tests.utils import _


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

    def _get_mocked_concurrency_packages(self, mock_cpu_count=4):
        multiprocessing_mock = MagicMock()
        multiprocessing_mock.cpu_count.return_value = mock_cpu_count

        concurrent_mock = MagicMock()
        thread_pool_executor_mock = concurrent_mock.futures.ThreadPoolExecutor
        thread_pool_executor_mock.return_value.__exit__.return_value = False

        modules = {
            'multiprocessing': multiprocessing_mock,
            'concurrent': concurrent_mock,
            'concurrent.futures': concurrent_mock.futures,
        }
        return modules, thread_pool_executor_mock

    def test_concurrency_setting(self):
        '''
        Setting PIPELINE_COMPILER_CONCURRENCY should override the default
        CPU count.
        '''
        modules, thread_pool_executor_mock = (
            self._get_mocked_concurrency_packages())

        settings.PIPELINE_COMPILER_CONCURRENCY = 2

        with patch.dict('sys.modules', modules):
            self.compiler.compile([])

        thread_pool_executor_mock.assert_called_once_with(
            max_workers=settings.PIPELINE_COMPILER_CONCURRENCY
        )

        settings.PIPELINE_COMPILER_CONCURRENCY = None

    def test_empty_concurrency_setting(self):
        '''
        Compiler should use cpu_count() if PIPELINE_COMPILER_CONCURRENCY is
        not set.
        '''
        MOCK_CPU_COUNT = 4
        modules, thread_pool_executor_mock = (
            self._get_mocked_concurrency_packages(MOCK_CPU_COUNT))

        with patch.dict('sys.modules', modules):
            self.compiler.compile([])

        thread_pool_executor_mock.assert_called_once_with(
            max_workers=MOCK_CPU_COUNT
        )

    def tearDown(self):
        settings.PIPELINE_COMPILERS = self.old_compilers
