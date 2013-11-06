from __future__ import unicode_literals

from django.test import TestCase

from pipeline.packager import Packager, PackageNotFound

from tests.utils import _


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
        self.assertEqual(packages['templates'].templates,
                         [_('pipeline/templates/photo/list.jst')])

    def test_package_compress(self):
        packager = Packager()
        packager.packages['js'] = packager.create_packages({
            'application': {
                'source_filenames': (
                    _('pipline/templates/application.js'),
                ),
                'output_filename': 'application.js',
            }
        })

        package = packager.package_for('js', 'application')
        self.assertTrue(package.compress)

        called = [False]

        # replace the method to check we get the right compressor
        def mock(package, compress, signal, **kwargs):
            self.assertNotEqual(compress, None)

            called[0] = True

        packager.pack = mock
        packager.pack_javascripts(package)

        self.assertTrue(called[0])

    def test_package_no_compress(self):
        packager = Packager()
        packager.packages['js'] = packager.create_packages({
            'application': {
                'source_filenames': (
                    _('pipline/templates/application.js'),
                ),
                'output_filename': 'application.js',
                'compress': False,
            }
        })

        package = packager.package_for('js', 'application')
        self.assertFalse(package.compress)

        called = [False]

        # replace the method to check we get the right compressor
        def mock(package, compress, signal, **kwargs):
            self.assertEqual(compress, None)

            called[0] = True

        packager.pack = mock
        packager.pack_javascripts(package)

        self.assertTrue(called[0])
