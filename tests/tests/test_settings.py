from __future__ import unicode_literals, print_function

from django.test import TestCase
from pipeline.conf import settings as pipeline_settings
from pipeline.conf.utils import get_groups
from tests import compressed
import imp
import tests

# The following imports the Django project settings module.
# Since pipeline will modify the attributes within that module,
# in order to test if pipeline did anything, the settings module
# is directly imported (which will contain the updates)
# Then that module is reloaded which will effectivelly reset
# it to its default state.
# Note: In order to be able to reload the module, the module
# is imported directly as compared to
# ``from django.conf import settings`` since that imports
# settings as a lazy object.
from tests import settings as original_settings


# reload the settings to get the original
original_settings = imp.reload(original_settings)


class SettingsTest(TestCase):
    def test_additional_apps(self):
        """
        Test that extra groups were indeed loaded into pipeline settings.
        """
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
        """
        Test that given an app module, ``get_groups`` returns correct
        group configurations.
        """
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
