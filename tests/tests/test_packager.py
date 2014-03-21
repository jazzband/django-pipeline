from __future__ import unicode_literals

from django.test import TestCase

from pipeline.collector import default_collector
from pipeline.packager import Packager, PackageNotFound

from tests.utils import _


class PackagerTest(TestCase):
    def setUp(self):
        default_collector.collect()

    def test_package_for(self):
        packager = Packager()
        packager.packages['js'] = packager.create_packages({
            'application': {
                'source_filenames': (
                    _('pipeline/js/application.js'),
                ),
                'output_filename': 'application.js'
            }
        })
        try:
            packager.package_for('js', 'application')
        except PackageNotFound:
            self.fail()
        try:
            packager.package_for('js', 'broken')
            self.fail()
        except PackageNotFound:
            pass

    def test_templates(self):
        packager = Packager()
        packages = packager.create_packages({
            'templates': {
                'source_filenames': (
                    _('pipeline/templates/photo/list.jst'),
                ),
                'output_filename': 'templates.js',
            }
        })
        self.assertEqual(packages['templates'].templates, [_('pipeline/templates/photo/list.jst')])

    def tearDown(self):
        default_collector.clear()
