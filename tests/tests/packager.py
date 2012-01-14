from django.test import TestCase

from pipeline.packager import Packager, PackageNotFound


class PackagerTest(TestCase):
    def test_package_for(self):
        packager = Packager()
        packager.packages['js'] = packager.create_packages({
            'application': {
                'source_filenames': (
                    'js/application.js',
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
                    'templates/photo/list.jst',
                ),
                'output_filename': 'templates.js',
            }
        })
        self.assertEqual(packages['templates'].templates, ['templates/photo/list.jst'])
