from django.test import TestCase

from pipeline.packager import Packager, PackageNotFound

from paths import _


class PackagerTest(TestCase):
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
