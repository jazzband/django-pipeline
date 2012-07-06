from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.utils import template_name
from os.path import splitext


class JadeCompiler(SubProcessCompiler):
    output_extension = 'js'

    def match_file(self, path):
        return path.endswith('.jade')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return  # File doesn't need to be recompiled
        if not outfile:
            path = splitext(infile)
            outfile = '.'.join((path[0], 'js'))

        js_before = '(function(){ %(namespace)s = %(namespace)s || {};\n' % {
            'namespace': settings.PIPELINE_TEMPLATE_NAMESPACE
        }
        js_after = '\n%s["%s"] = anonymous;})();' % (
            settings.PIPELINE_TEMPLATE_NAMESPACE,
            template_name(infile),
        )

        command = "echo '%s' > %s ; %s -c %s < %s >> %s ; echo '%s' >> %s" % (
            js_before,
            outfile,
            settings.PIPELINE_JADE_BINARY,
            settings.PIPELINE_JADE_ARGUMENTS,
            infile,
            outfile,
            js_after,
            outfile,
        )
        return self.execute_command(command)
