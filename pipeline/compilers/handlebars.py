from pipeline.conf import settings
from pipeline.compilers import TemplateCompiler
from pipeline.utils import template_name


class HandlebarsCompiler(TemplateCompiler):
    input_extension = '.handlebars'
    js_compile_function = 'Handlebars.compile'
    js_template_adder = ''

    def compile_to_js(self, infile, outfile, in_relative_path):
        js_before = '''
(function(){ %(namespace)s = %(namespace)s || {};
%(namespace)s["%(name)s"] = Handlebars.template(''' % {
            'namespace': settings.PIPELINE_TEMPLATE_NAMESPACE,
            'name': template_name(in_relative_path, '', self.input_extension),
        }
        js_after = ');\n)();'

        command = "echo -n '%s' > %s ; %s %s -s %s >> %s ; echo '%s' >> %s" % (
            js_before,
            outfile,
            settings.PIPELINE_HANDLEBARS_BINARY,
            infile,
            settings.PIPELINE_HANDLEBARS_ARGUMENTS,
            outfile,
            js_after,
            outfile,
        )
        return self.execute_command(command)
