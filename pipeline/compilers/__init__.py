import os
import subprocess

try:
    from staticfiles import finders
except ImportError:
    from django.contrib.staticfiles import finders # noqa

from django.core.files.base import ContentFile
from django.utils.encoding import smart_str

from pipeline.conf import settings
from pipeline.storage import default_storage
from pipeline.utils import to_class


class Compiler(object):
    def __init__(self, storage=default_storage, verbose=False):
        self.storage = storage
        self.verbose = verbose

    def compilers(self):
        return [to_class(compiler) for compiler in settings.PIPELINE_COMPILERS]
    compilers = property(compilers)

    def compile(self, paths):
        for index, path in enumerate(paths):
            for compiler in self.compilers:
                compiler = compiler(self.verbose)
                if compiler.match_file(path):
                    new_path = self.output_path(path, compiler.output_extension)
                    content = self.read_file(path)
                    try:
                        compiled_content = compiler.compile_file(content, finders.find(path))
                        self.save_file(new_path, compiled_content)
                    except CompilerError:
                        if not self.storage.exists(new_path) or not settings.PIPELINE:
                            raise
                    paths[index] = new_path
        return paths

    def output_path(self, path, extension):
        path = os.path.splitext(path)
        return '.'.join((path[0], extension))

    def read_file(self, path):
        file = self.storage.open(path, 'rb')
        content = file.read()
        file.close()
        return content

    def save_file(self, path, content):
        return self.storage.save(path, ContentFile(smart_str(content)))


class CompilerBase(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def match_file(self, filename):
        raise NotImplementedError

    def compile_file(self, content, path):
        raise NotImplementedError


class CompilerError(Exception):
    pass


class SubProcessCompiler(CompilerBase):
    def execute_command(self, command, content=None, cwd=None):
        pipe = subprocess.Popen(command, shell=True, cwd=cwd,
            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE)

        if content:
            pipe.stdin.write(content)
            pipe.stdin.close()

        compressed_content = pipe.stdout.read()
        pipe.stdout.close()

        error = pipe.stderr.read()
        pipe.stderr.close()

        if pipe.wait() != 0:
            if not error:
                error = "Unable to apply %s compiler" % self.__class__.__name__
            raise CompilerError(error)

        if self.verbose:
            print error

        return compressed_content
