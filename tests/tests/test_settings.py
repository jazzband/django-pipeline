from __future__ import unicode_literals

from django.test import TestCase
from pipeline.conf import settings as pipeline_settings
from pipeline.conf.utils import get_groups
from tests import compressed
import imp
import tests

# The following imports the Django project settings module.
# Since pipeline will modify the attributes within that module,
# in order to test if pipeline did anything, a copy of all module's
# attributes is cached. Then the whole module is reloaded from
# scratch to load the original settings as they are defined
# within the file. That is also the reason why the direct module
# from tests is imported compared to doing
# ``from django.conf import settings`` because Python's ``reload``
# only works on modules.
from tests import settings


class Dummy(object):
    pass


django_settings = Dummy()
for k, v in vars(settings).items():
    setattr(django_settings, k, v)

# this reloads the settings to get the original
original_settings = imp.reload(settings)


class SettingsTest(TestCase):
    def test_additional_apps(self):
        for attr in ['css', 'js']:
            attr = 'PIPELINE_{0}'.format(attr.upper())
            self.assertNotEqual(
                len(getattr(pipeline_settings, attr)),
                len(getattr(original_settings, attr)),
            )

            self.assertEqual(
                len(getattr(pipeline_settings, attr)),
                len(getattr(original_settings, attr)) + len(getattr(compressed, attr)),
            )

    def test_get_groups(self):
        app_module = tests
        pipeline_module = 'compressed'
        namespace = False
        namespace_format = '{app_label}_{group_key}'

        groups = get_groups(app_module,
                            pipeline_module,
                            namespace,
                            namespace_format)

        for i in ['css', 'js']:
            attr = 'PIPELINE_{0}'.format(i.upper())
            self.assertEqual(groups[i].keys(),
                             getattr(compressed, attr).keys())

        namespace = True
        groups = get_groups(app_module,
                            pipeline_module,
                            namespace,
                            namespace_format)

        for i in ['css', 'js']:
            attr = 'PIPELINE_{0}'.format(i.upper())
            self.assertNotEqual(groups[i].keys(),
                                getattr(compressed, attr).keys())

            keys = [namespace_format.format(app_label='tests', group_key=key)
                    for key in getattr(compressed, attr).keys()]
            self.assertEqual(list(groups[i].keys()), keys)
