import os
import subprocess
import re

try:
    from staticfiles import finders
except ImportError:
    from django.contrib.staticfiles import finders # noqa

from pipeline.conf import settings
from pipeline.storage import default_storage
from pipeline.utils import to_class, template_name, read_file, write_file


class Compiler(object):
    def __init__(self, storage=default_storage, verbose=False):
        self.storage = storage
        self.verbose = verbose

    def compilers(self):
        return [to_class(compiler) for compiler in settings.PIPELINE_COMPILERS]
    compilers = property(compilers)

    def compile(self, paths, force=False):
        for index, input_path in enumerate(paths):
            for compiler in self.compilers:
                compiler = compiler(self.verbose)
                if compiler.match_file(input_path):
                    output_path = self.output_path(input_path, compiler.output_extension)
                    paths[index] = output_path
                    try:
                        infile = finders.find(input_path)
                        outfile = finders.find(output_path)
                        if outfile is None:
                            outfile = self.output_path(infile, compiler.output_extension)
                            outdated = True
                        else:
                            outdated = self.is_outdated(input_path, output_path)
                        if isinstance(compiler, TemplateCompiler):
                            compiler.compile_file(infile, outfile, input_path,
                                                  outdated=outdated, force=force)
                        else:
                            compiler.compile_file(infile, outfile, outdated=outdated,
                                                  force=force)
                    except CompilerError:
                        if not self.storage.exists(output_path) or not settings.PIPELINE:
                            raise
        return paths

    def output_path(self, path, extension):
        path = os.path.splitext(path)
        return '.'.join((path[0], extension))

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


class TemplateCompiler(SubProcessCompiler):
    output_extension = 'js'
    js_embed_wrap = '''
%(namespace)s = %(namespace)s || {};
%(namespace)s['%(name)s'] = %(js_compile_fn)s('%(content)s');
'''

    def match_file(self, path):
        return path.endswith(self.input_extension)

    def compile_file(self, infile, outfile, infile_relative_path,
                     outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled

        if settings.PIPELINE_TEMPLATE_COMPILE:
            return self.compile_to_js(infile, outfile, infile_relative_path)
        else:
            return self.concatenate_to_js(infile, outfile, infile_relative_path)

    def compile_to_js(self, infile, outfile, infile_relative_path):
        raise NotImplementedError

    def concatenate_to_js(self, infile, outfile, infile_relative_path):
        contents = read_file(infile_relative_path)
        contents = re.sub(r"\n", "\\\\n", contents)
        contents = re.sub(r"'", "\\'", contents)

        name = template_name(infile_relative_path, '', self.input_extension)

        contents = self.js_embed_wrap % {
            'namespace': settings.PIPELINE_TEMPLATE_NAMESPACE,
            'name': name,
            'content': contents,
            'js_compile_fn': self.js_compile_function,
        }

        write_file(outfile, contents)
