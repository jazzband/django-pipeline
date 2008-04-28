# {% %}
from django import template
from django.conf import settings

register = template.Library()

def render_css(css, filename):
    return template.loader.render_to_string('compress/css.html', {
        'url': settings.MEDIA_URL + filename,
        'css': css,
    })

def render_js(js, filename):
    return template.loader.render_to_string('compress/js.html', {
        'url': settings.MEDIA_URL + filename,
        'js': js,
    })

class CompressedCSSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        css_name = template.Variable(self.name).resolve(context)
        css = settings.COMPRESS_CSS[css_name]
        if settings.COMPRESS:
            return render_css(css, css['compressed_filename'])
        else:
            # output source files
            r = ''
            for source_file in css['source_filenames']:
                r += render_css(css, source_file)

            return r

class CompressedJSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        js_name = template.Variable(self.name).resolve(context)
        js = settings.COMPRESS_JS[js_name]
        if settings.COMPRESS:
            return render_js(js, js['compressed_filename'])
        else:
            # output source files
            r = ''
            for source_file in js['source_filenames']:
                r += render_js(js, source_file)
            return r

# @register.tag
def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument, being the name of the COMPRESS_CSS setting'

    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)

# @register.tag
def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument, being the name of the COMPRESS_JS setting'

    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)