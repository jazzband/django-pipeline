import os
import subprocess

try:
    from staticfiles import finders
except ImportError:
    from django.contrib.staticfiles import finders # noqa

from pipeline.conf import settings
from pipeline.storage import default_storage
from pipeline.utils import to_class


class Compiler(object):
    def __init__(self, storage=default_storage, verbose=False):
        self.storage = storage
        self.verbose = verbose

    @property
    def compilers(self):
        return [to_class(compiler) for compiler in settings.PIPELINE_COMPILERS]

    @property
    def precompilers(self):
        return [to_class(precompiler) for precompiler in settings.PIPELINE_PRECOMPILERS]

    def compile(self, paths, force=False):
        paths = self.compile_paths(paths, self.precompilers, force=force)
        paths = self.compile_paths(paths, self.compilers, force=force)
        return paths

    def compile_paths(self, paths, compilers, force=False):
        for index, input_path in enumerate(paths):
            for compiler in compilers:
                compiler = compiler(self.verbose)
                if compiler.match_file(input_path):
                    output_path = compiler.output_path(input_path)
                    paths[index] = output_path
                    try:
                        infile = finders.find(input_path)
                        outfile = finders.find(output_path)
                        outdated = self.is_outdated(input_path, output_path)
                        compiler.compile_file(infile, outfile, outdated=outdated, force=force)
                    except CompilerError:
                        if not self.storage.exists(output_path) or not settings.PIPELINE:
                            raise
                    input_path = output_path
        return paths

    def is_outdated(self, infile, outfile):
        try:
            return self.storage.modified_time(infile) > self.storage.modified_time(outfile)
        except (OSError, NotImplementedError):
            return True


class CompilerBase(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def match_file(self, filename):
        raise NotImplementedError

    def compile_file(self, infile, outfile, outdated=False, force=False):
        raise NotImplementedError

    def output_path(self, path):
        path = os.path.splitext(path)
        return '.'.join((path[0], self.output_extension))


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
