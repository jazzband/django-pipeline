from __future__ import unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from pipeline.collector import default_collector
from pipeline.views import serve_static
from tests.utils import pipeline_settings


@override_settings(DEBUG=True)
@pipeline_settings(PIPELINE_COLLECTOR_ENABLED=True, PIPELINE_ENABLED=False)
class ServeStaticViewsTest(TestCase):
    def setUp(self):
        super(ServeStaticViewsTest, self).setUp()

        self.filename = 'pipeline/js/first.js'
        self.storage = staticfiles_storage
        self.request = RequestFactory().get('/static/%s' % self.filename)

        default_collector.clear()

    def tearDown(self):
        super(ServeStaticViewsTest, self).tearDown()

        default_collector.clear()
        staticfiles_storage._setup()

    def test_found(self):
        self._test_found()

    def test_not_found(self):
        self._test_not_found('missing-file')

    @override_settings(DEBUG=False)
    def test_debug_false(self):
        with self.assertRaises(ImproperlyConfigured):
            serve_static(self.request, self.filename)

        self.assertFalse(self.storage.exists(self.filename))

    @override_settings(DEBUG=False)
    def test_debug_false_and_insecure(self):
        self._test_found(insecure=True)

    @pipeline_settings(PIPELINE_ENABLED=True)
    def test_pipeline_enabled_and_found(self):
        self._write_content()
        self._test_found()

    @pipeline_settings(PIPELINE_ENABLED=True)
    def test_pipeline_enabled_and_not_found(self):
        self._test_not_found(self.filename)

    @pipeline_settings(PIPELINE_COLLECTOR_ENABLED=False)
    def test_collector_disabled_and_found(self):
        self._write_content()
        self._test_found()

    @pipeline_settings(PIPELINE_COLLECTOR_ENABLED=False)
    def test_collector_disabled_and_not_found(self):
        self._test_not_found(self.filename)

    def _write_content(self, content='abc123'):
        """Write sample content to the test static file."""
        with self.storage.open(self.filename, 'w') as f:
            f.write(content)

    def _test_found(self, **kwargs):
        """Test that a file can be found and contains the correct content."""
        response = serve_static(self.request, self.filename, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.storage.exists(self.filename))

        if hasattr(response, 'streaming_content'):
            content = b''.join(response.streaming_content)
        else:
            content = response.content

        with self.storage.open(self.filename) as f:
            self.assertEqual(f.read(), content)

    def _test_not_found(self, filename):
        """Test that a file could not be found."""
        self.assertFalse(self.storage.exists(filename))

        with self.assertRaises(Http404):
            serve_static(self.request, filename)

        self.assertFalse(self.storage.exists(filename))
