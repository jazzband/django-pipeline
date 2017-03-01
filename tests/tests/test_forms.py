from __future__ import unicode_literals

from django.forms import Media
from django.test import TestCase
from django.utils import six

from pipeline.forms import PipelineFormMedia
from ..utils import pipeline_settings


@pipeline_settings(
    PIPELINE_COLLECTOR_ENABLED=False,
    STYLESHEETS={
        'styles1': {
            'source_filenames': (
                'pipeline/css/first.css',
                'pipeline/css/second.css',
            ),
            'output_filename': 'styles1.min.css',
        },
        'styles2': {
            'source_filenames': (
                'pipeline/css/unicode.css',
            ),
            'output_filename': 'styles2.min.css',
        },
        'print': {
            'source_filenames': (
                'pipeline/css/urls.css',
            ),
            'output_filename': 'print.min.css',
        },
    },
    JAVASCRIPT={
        'scripts1': {
            'source_filenames': (
                'pipeline/js/first.js',
                'pipeline/js/second.js',
            ),
            'output_filename': 'scripts1.min.js',
        },
        'scripts2': {
            'source_filenames': (
                'pipeline/js/application.js',
            ),
            'output_filename': 'scripts2.min.js',
        },
    })
class PipelineFormMediaTests(TestCase):
    """Unit tests for pipeline.forms.PipelineFormMedia."""

    @pipeline_settings(PIPELINE_ENABLED=True)
    def test_css_packages_with_pipeline_enabled(self):
        """Testing PipelineFormMedia.css_packages with PIPELINE_ENABLED=True"""
        class MyMedia(PipelineFormMedia):
            css_packages = {
                'all': ('styles1', 'styles2'),
                'print': ('print',),
            }

            css = {
                'all': ('extra1.css', 'extra2.css')
            }

        media = Media(MyMedia)

        self.assertEqual(
            MyMedia.css,
            {
                'all': [
                    'extra1.css',
                    'extra2.css',
                    '/static/styles1.min.css',
                    '/static/styles2.min.css',
                ],
                'print': ['/static/print.min.css'],
            })
        self.assertEqual(MyMedia.css, media._css)
        self.assertEqual(
            list(media.render_css()),
            [
                '<link href="%s" type="text/css" media="all" '
                'rel="stylesheet" />' % path
                for path in (
                    '/static/extra1.css',
                    '/static/extra2.css',
                    '/static/styles1.min.css',
                    '/static/styles2.min.css',
                )
            ] + [
                '<link href="/static/print.min.css" type="text/css" '
                'media="print" rel="stylesheet" />'
            ])

    @pipeline_settings(PIPELINE_ENABLED=False)
    def test_css_packages_with_pipeline_disabled(self):
        """Testing PipelineFormMedia.css_packages with PIPELINE_ENABLED=False"""
        class MyMedia(PipelineFormMedia):
            css_packages = {
                'all': ('styles1', 'styles2'),
                'print': ('print',),
            }

            css = {
                'all': ('extra1.css', 'extra2.css')
            }

        media = Media(MyMedia)

        self.assertEqual(
            MyMedia.css,
            {
                'all': [
                    'extra1.css',
                    'extra2.css',
                    'pipeline/css/first.css',
                    'pipeline/css/second.css',
                    'pipeline/css/unicode.css',
                ],
                'print': ['pipeline/css/urls.css'],
            })
        self.assertEqual(MyMedia.css, media._css)
        self.assertEqual(
            list(media.render_css()),
            [
                '<link href="%s" type="text/css" media="all" '
                'rel="stylesheet" />' % path
                for path in (
                    '/static/extra1.css',
                    '/static/extra2.css',
                    '/static/pipeline/css/first.css',
                    '/static/pipeline/css/second.css',
                    '/static/pipeline/css/unicode.css',
                )
            ] + [
                '<link href="/static/pipeline/css/urls.css" type="text/css" '
                'media="print" rel="stylesheet" />'
            ])

    @pipeline_settings(PIPELINE_ENABLED=True)
    def test_js_packages_with_pipeline_enabled(self):
        """Testing PipelineFormMedia.js_packages with PIPELINE_ENABLED=True"""
        class MyMedia(PipelineFormMedia):
            js_packages = ('scripts1', 'scripts2')
            js = ('extra1.js', 'extra2.js')

        media = Media(MyMedia)

        self.assertEqual(
            MyMedia.js,
            [
                'extra1.js',
                'extra2.js',
                '/static/scripts1.min.js',
                '/static/scripts2.min.js',
            ])
        self.assertEqual(MyMedia.js, media._js)
        self.assertEqual(
            media.render_js(),
            [
                '<script type="text/javascript" src="%s"></script>' % path
                for path in (
                    '/static/extra1.js',
                    '/static/extra2.js',
                    '/static/scripts1.min.js',
                    '/static/scripts2.min.js',
                )
            ])

    @pipeline_settings(PIPELINE_ENABLED=False)
    def test_js_packages_with_pipeline_disabled(self):
        """Testing PipelineFormMedia.js_packages with PIPELINE_ENABLED=False"""
        class MyMedia(PipelineFormMedia):
            js_packages = ('scripts1', 'scripts2')
            js = ('extra1.js', 'extra2.js')

        media = Media(MyMedia)

        self.assertEqual(
            MyMedia.js,
            [
                'extra1.js',
                'extra2.js',
                'pipeline/js/first.js',
                'pipeline/js/second.js',
                'pipeline/js/application.js',
            ])
        self.assertEqual(MyMedia.js, media._js)
        self.assertEqual(
            media.render_js(),
            [
                '<script type="text/javascript" src="%s"></script>' % path
                for path in (
                    '/static/extra1.js',
                    '/static/extra2.js',
                    '/static/pipeline/js/first.js',
                    '/static/pipeline/js/second.js',
                    '/static/pipeline/js/application.js',
                )
            ])
