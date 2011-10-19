from django import template
from django.template.loader import render_to_string

from pipeline.conf import settings
from pipeline.templatetags.modernizr import CompressedJSNode

register = template.Library()


class ModernizrJSNode(CompressedJSNode):
    def render_js(self, package, path):
        context = {}
        if not 'template' in package:
            package['template'] = "pipeline/js.html"
        if 'context' in package:
            context = package['context']
        context.update({
            'url': self.packager.individual_url(path)
        })
        return render_to_string(package['template'], context)

    def render_external(self, package, url):
        if not 'template' in package:
            package['template'] = "pipeline/js.html"
        return render_to_string(package['template'], {
            'url': url
        })

    def render_inline(self, package, js):
        context = {}
        if 'context' in package:
            context = package['context']
        context.update({
            'source': js
        })
        return render_to_string("pipeline/inline_js.html", context)

    def render_individual(self, package, templates=None):
        tags = [self.render_js(package, js) for js in package['paths']]
        if templates:
            tags.append(self.render_inline(package, templates))
        return '\n'.join(tags)


def modernizr_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the PIPELINE_JS setting' % token.split_contents()[0]
    return ModernizrJSNode(name)

modernizr_js = register.tag(modernizr_js)
