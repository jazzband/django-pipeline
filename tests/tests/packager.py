import os

from django.test import TestCase

from pipeline.conf import settings
from pipeline.packager import Packager


class PackagerTest(TestCase):
    def setUp(self):
        self.old_pipeline_url = settings.PIPELINE_URL
        settings.PIPELINE_URL = 'http://localhost/static/'

    def test_individual_url(self):
        """Check that individual URL is correctly generated"""
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
                'output': 'application.r?.js',
                'paths': ['js/application.js'],
                'templates': []
            }
        })

    def tearDown(self):
        settings.PIPELINE_URL = self.old_pipeline_url
