import os

from django.test import TestCase

from pipeline.conf import settings
from pipeline.packager import Packager, PackageNotFound


class PackagerTest(TestCase):
    def setUp(self):
        self.old_pipeline_url = settings.PIPELINE_URL
        settings.PIPELINE_URL = 'http://localhost/static/'

    def test_package_for(self):
        packager = Packager()
        packager.packages['js'] = packager.create_packages({
            'application': {
                'source_filenames': (
                    'js/application.js',
                ),
                'output_filename': 'application.r?.js'
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
                'output_filename': 'templates.r?.js',
            }
        })
        self.assertEqual(packages, {
            'templates': {
                'templates': ['templates/photo/list.jst'],
                'manifest': True,
                'paths': [],
                'context': {},
                'output': 'templates.r?.js'
            }
        })

    def test_individual_url(self):
        """Check that individual URL is correctly generated"""
        packager = Packager()
        filename = os.path.join(settings.PIPELINE_ROOT, u'js/application.js')
        individual_url = packager.individual_url(filename)
        self.assertEqual(individual_url,
            "http://localhost/static/js/application.js")

    def test_periods_safe_individual_url(self):
        """Check that the periods in file names do not get replaced by individual_url when
        PIPELINE_ROOT/STATIC_ROOT is not set, such as in development
        """
        settings.PIPELINE_ROOT = settings.STATIC_ROOT = settings.MEDIA_ROOT = ""
        packager = Packager()
        filename = os.path.join(settings.PIPELINE_ROOT, u'js/application.js')
        individual_url = packager.individual_url(filename)
        self.assertEqual(individual_url,
            "http://localhost/static/js/application.js")

    def test_external_urls(self):
        packager = Packager()
        packages = packager.create_packages({
            'jquery': {
                'external_urls': ('//ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js',)
            },
            'application': {
                'source_filenames': ('js/application.js',),
                'output_filename': 'application.r?.js'
            }
        })
        self.assertEqual(packages, {
            'jquery': {
                'externals': ('//ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js',)
            },
            'application': {
                'context': {},
                'manifest': True,
                'output': 'application.r?.js',
                'paths': ['js/application.js'],
                'templates': []
            }
        })

    def tearDown(self):
        settings.PIPELINE_URL = self.old_pipeline_url
