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
tempalte tags so it would benefit from a refactor.
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

_settings = None


def get_settings():
    """ Because extra Jinja2 functions have to be declared
    at creation time the new functions have to be declared before
    django settings evaluation so when pipeline tries to import django
    settings it will get the default globals rather than user defined settings.
    This function attempts to fudge back in user defined settings into
    pipeline settings as django.conf.settings is lazy loaded and pipeline
    settings are not.

    Pleae don't hurt me :(

    I guess a better more robust solution would be to make pipeline settings
    lazy loaded also."""

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
    _settings = pipeline_settings
    return _settings


def get_css_package(package_name):
    """ Get the package from pipeline settings."""

    settings = get_settings() if not _settings else _settings  # Get settings
    package = settings.PIPELINE_CSS.get(package_name, {})
    if package:
        package = {package_name: package}
    packager = Packager(css_packages=package, js_packages={})
    try:
        package = packager.package_for('css', package_name)
    except PackageNotFound:
        return None
    return (package, packager)


def get_js_package(package_name):
    """ Get the package from pipeline settings."""

    settings = get_settings() if not _settings else _settings  # Get settings
    package = settings.PIPELINE_JS.get(package_name, {})
    if package:
        package = {package_name: package}
    packager = Packager(css_packages={}, js_packages=package)
    try:
        package = packager.package_for('js', package_name)
    except PackageNotFound:
        return None
    return (package, packager)


# TODO: render_css and render_js are very similar - refactor together?
def render_css(package, path):
    from django.template.loaders import app_directories
    loader = FileSystemLoader(
            app_directories.app_template_dirs + django_settings.TEMPLATE_DIRS)
    template_name = package.template_name or "pipeline/css.jinja"
    context = package.extra_context
    context.update({
        'type': guess_type(path, 'text/css'),
        'url': staticfiles_storage.url(path)
    })
    env = Environment(loader=loader)
    tpl = env.get_template(template_name)
    return tpl.render(**context)


def render_individual_css(package, paths):
    tags = [render_css(package, path) for path in paths]
    return '\n'.join(tags)


def render_js(package, path):
    from django.template.loaders import app_directories
    loader = FileSystemLoader(
            app_directories.app_template_dirs + django_settings.TEMPLATE_DIRS)
    template_name = package.template_name or "pipeline/js.jinja"
    context = package.extra_context
    context.update({
        'type': guess_type(path, 'text/javascript'),
        'url': staticfiles_storage.url(path)
    })
    env = Environment(loader=loader)
    tpl = env.get_template(template_name)
    return tpl.render(**context)


def render_inline(package, js):
    from django.template.loaders import app_directories
    loader = FileSystemLoader(
            app_directories.app_template_dirs + django_settings.TEMPLATE_DIRS)
    template_name = package.template_name or "pipeline/inline_js.jinja"
    context = package.extra_context
    context.update({
        'source': js
    })
    env = Environment(loader=loader)
    tpl = env.get_template(template_name)
    return tpl.render(**context)


def render_individual_js(package, paths, templates=None):
    tags = [render_js(package, path) for path in paths]
    if templates:
        tags.append(render_inline(package, templates))
    return '\n'.join(tags)


def compressed_css(package_name):
    settings = get_settings() if not _settings else _settings  # Get settings
    package, packager = get_css_package(package_name)
    if package:
        if settings.PIPELINE:
            return render_css(package, package.output_filename)
        else:
            paths = packager.compile(package.paths)
            return render_individual_css(package, paths)
    else:
        return ''


def compressed_js(package_name):
    settings = get_settings() if not _settings else _settings  # Get settings
    package, packager = get_js_package(package_name)
    if package:
        if settings.PIPELINE:
            return render_js(package, package.output_filename)
        else:
            paths = packager.compile(package.paths)
            templates = packager.pack_templates(package)
            return render_individual_js(package, paths, templates)
    else:
        return ''
