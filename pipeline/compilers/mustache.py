from pipeline.compilers import TemplateCompiler


class MustacheCompiler(TemplateCompiler):
    input_extension = '.mustache'
    js_compile_function = 'Mustache.template'
    js_template_adder = '''
Mustache.template = function(templateString) {
  return function() {
    if (arguments.length < 1) {
      return templateString;
    } else {
      return Mustache.render(templateString, arguments[0], arguments[1]);
    }
  };
};
'''
