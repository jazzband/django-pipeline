import subprocess

class CompilerBase(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def match_file(self, filename):
        raise NotImplementedError

    def compile_file(self, content):
        raise NotImplementedError


class CompilerError(Exception):
    pass


class SubProcessCompiler(CompilerBase):
    def execute_command(self, command, content):
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        pipe.stdin.write(content)
        pipe.stdin.close()

        compressed_content = pipe.stdout.read()
        pipe.stdout.close()

        error = pipe.stderr.read()
        pipe.stderr.close()

        if pipe.wait() != 0:
            if not error:
                error = "Unable to apply %s compiler" % self.__class__.__name__
            raise FilterError(error)

        if self.verbose:
            print error

        return compressed_content
