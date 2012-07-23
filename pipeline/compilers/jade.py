from pipeline.conf import settings
from pipeline.compilers import TemplateCompiler
from pipeline.utils import template_name


class JadeCompiler(TemplateCompiler):
    output_extension = 'js'
    js_wrap_concatenated = '''
%(namespace)s = %(namespace)s || {};
%(namespace)s['%(name)s'] = jade.compile('%(content)s', {compileDebug: false});
'''

    def match_file(self, path):
        return path.endswith('.jade')

    def compile_to_js(self, infile, outfile, in_relative_path):
        js_before = '(function(){ %(namespace)s = %(namespace)s || {};\n' % {
            'namespace': settings.PIPELINE_TEMPLATE_NAMESPACE
        }
        js_after = '\n%s["%s"] = anonymous;})();' % (
            settings.PIPELINE_TEMPLATE_NAMESPACE,
            template_name(in_relative_path, ''),
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
