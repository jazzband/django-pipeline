from __future__ import unicode_literals

from django.db.models.loading import get_apps
from django.utils.importlib import import_module


def get_app_module(app):
    """
    Get the actual app module. This is similar to Django's ``get_app`` function from
    ``django.db.models.loading.get_app`` however instead of returning the model's
    module, this function returns the actual app module.
    """
    return import_module(app.__name__.rsplit('.', 1)[0])


def get_app_modules():
    """
    Get modules of all installed apps. This is similar to Django's ``get_apps`` function
    from ``django.db.models.loading.get_apps`` however instead of returning the model's
    modules, this function returns modules of the actual app.
    """
    return [get_app_module(app) for app in get_apps()]


def get_app_label(app_module):
    """
    Get the app label name from the app module
    """
    return app_module.__name__.rsplit('.', 1)[-1]


def get_module_from_package(package, module, default=None):
    """
    Return the specified module from the given package.
    """
    try:
        return import_module('{0}.{1}'.format(package.__name__, module))
    except ImportError:
        return default


def get_groups(app_module,
               pipeline_module,
               namespace,
               namespace_format):
    """
    Return all the groups from the app pipeline module. This function also
    renames the group keys if necessary so the output of this function can
    safely be merged (``dict.update``) with the main project pipeline
    settings.
    """
    pipeline_module = get_module_from_package(app_module, pipeline_module)

    if not pipeline_module:
        return {
            'css': {},
            'js': {},
        }

    css = getattr(pipeline_module, 'PIPELINE_CSS', {})
    js = getattr(pipeline_module, 'PIPELINE_JS', {})

    if namespace:
        app_label = get_app_label(app_module)

        css_keys = [namespace_format.format(app_label=app_label, group_key=key)
                    for key in css.keys()]
        js_keys = [namespace_format.format(app_label=app_label, group_key=key)
                   for key in js.keys()]

        css = dict(zip(css_keys, css.values()))
        js = dict(zip(js_keys, js.values()))

    return {
        'css': css,
        'js': js,
    }
