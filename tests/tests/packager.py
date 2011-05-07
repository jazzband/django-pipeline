import os

from django.test import TestCase

from compress.conf import settings
from compress.packager import Packager


class PackagerTest(TestCase):
    def setUp(self):
        self.old_compress_url = settings.COMPRESS_URL
        settings.COMPRESS_URL = 'http://localhost/static/'

    def test_individual_url(self):
        """Check that individual URL is correctly generated"""
        packager = Packager()
        filename = os.path.join(settings.COMPRESS_ROOT, u'js/application.js')
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
                'paths': ['js/application.js']
            }
        })

    def tearDown(self):
        settings.COMPRESS_URL = self.old_compress_url
