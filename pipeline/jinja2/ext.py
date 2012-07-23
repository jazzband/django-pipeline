"""
Jinja 2 Template Functions

Warning: This is experimental.

Takes the basis of whats in pipeline.templattags.compressed and applies to
jinja2 templates in the form of a global function. You need to expose this
functions to the jinja2 environment yourself.

Example:
    {{ compressed_css('group_name') }}
    {{ compressed_js('group_name') }}

Note: There is quite a bit of code duplication here from whats in the django
template tags so it would benefit from a refactor.
"""

import inspect

try:
    from staticfiles.storage import staticfiles_storage
except ImportError:
    from django.contrib.staticfiles.storage import staticfiles_storage

from django.conf import settings as django_settings
from jinja2 import Environment, FileSystemLoader
from pipeline.conf import settings as pipeline_settings
from pipeline.packager import Packager, PackageNotFound
from pipeline.utils import guess_type


class Jinja2Compressed(object):

    def __init__(self, ftype):
        """ Constructor, sets up object.

        @arg1: str: file type (css/js)
        """

        from django.template.loaders import app_directories  # has to be here
        if ftype not in ['css', 'js']:
            raise Exception('Package type must be css or js, supplied '
                            '%s' % ftype)
        self.ftype = ftype
        self.loader = FileSystemLoader((app_directories.app_template_dirs +
            django_settings.TEMPLATE_DIRS))
        self.get_pipeline_settings()

    def get_pipeline_settings(self):
        """ Because extra Jinja2 functions have to be declared
        at creation time the new functions have to be declared before
        django settings evaluation so when pipeline tries to import django
        settings it will get the default globals rather than user defined
        settings. This function attempts to fudge back in user defined
        settings into pipeline settings as django.conf.settings is lazy
        loaded and pipeline settings are not.

        Pleae don't hurt me :(

        I guess a better more robust solution would be to make pipeline
        settings lazy loaded also."""

        members = inspect.getmembers(pipeline_settings)
        for setting, val in members:
            if setting.startswith('PIPELINE'):
                if hasattr(django_settings, setting):
                    val = getattr(django_settings, setting)
                else:
                    if type(getattr(pipeline_settings, setting)) == str:
                        val = "'%s'" % val
                val = val if val else "''"
                expr = "pipeline_settings.%s = %s" % (
                        setting, val)
                exec expr
            pipeline_settings.PIPELINE = getattr(django_settings,
                    'PIPELINE', not django_settings.DEBUG)
        self.settings = pipeline_settings

    def get_package(self, name):
        """ Get the js or css package.

        @arg1: str: name of the package to get
        """

        package = {
            'js':   self.settings.PIPELINE_JS.get(name, {}),
            'css':  self.settings.PIPELINE_CSS.get(name, {}),
        }[self.ftype]

        if package:
            package = {name: package}

        self.packager = {
            'js':   Packager(css_packages={}, js_packages=package),
            'css':  Packager(css_packages=package, js_packages={}),
        }[self.ftype]

        try:
            self.package = self.packager.package_for(self.ftype, name)
        except PackageNotFound:
            self.package = None

    def render(self, path):
        """ Render the HTML tag.

        @arg1: str: path to file

        return str: the HTML output
        """

        if not self.package.template_name:
            template_name = {
                'js':   'pipeline/js.jinja',
                'css':  'pipeline/css.jinja',
            }[self.ftype]
        else:
            template_name = self.package.template_name

        mimetype = {
            'js':   'text/javascript',
            'css':  'text/css',
        }[self.ftype]

        context = self.package.extra_context
        context.update({
            'type': guess_type(path, mimetype),
            'url': staticfiles_storage.url(path)
        })

        env = Environment(loader=self.loader)
        tpl = env.get_template(template_name)
        return tpl.render(**context)

    def html(self, name):
        """ Render the HTML Snippet

        @arg1: str: package name

        return: str: HTML snippet
        """

        self.get_package(name)
        if self.package:
            if self.settings.PIPELINE:
                return self.render(self.package.output_filename)
            else:
                paths = self.packager.compile(self.package.paths)
                templates = self.packager.pack_templates(self.package)
                return {
                    'css': self.render_individual_css(paths),
                    'js': self.render_individual_js(paths, templates)
                }[self.ftype]
        else:
            return ''  # don't return anything if no package found

    def render_individual_css(self, paths):
        """ Render individual CSS files, for when PIPELINE = False

        @arg1: list: paths to css files

        return: str: rendered individual css tags
        """

        tags = [self.render(path) for path in paths]
        return '\n'.join(tags)

    def render_individual_js(self, paths, templates=None):
        """ Render individual JS files, for when PIPELINE = False

        @arg1: list: paths to js files

        return: str: rendered individual script tags
        """

        tags = [self.render(path) for path in paths]
        if templates:
            tags.append(self.render_inline_js(self.package, templates))
        return '\n'.join(tags)

    def render_inline_js(self, package, js):
        template_name = (self.package.template_name or
                "pipeline/inline_js.jinja")
        context = self.package.extra_context
        context.update({
            'source': js
        })
        env = Environment(loader=self.loader)
        tpl = env.get_template(template_name)
        return tpl.render(**context)


def compressed_css(package_name):
    """ Compress css Jinja2 function,
    {{ compressed_css('a_group') }}
    """

    compress = Jinja2Compressed('css')
    return compress.html(package_name)


def compressed_js(package_name):
    """ Compress js Jinja2 function,
    {{ compressed_js('a_group') }}
    """

    compress = Jinja2Compressed('js')
    return compress.html(package_name)
