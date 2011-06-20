from mock import patch

from django.test import TestCase

from pipeline.conf import settings
from pipeline.storage import storage
from pipeline.versioning import Versioning
from pipeline.versioning.mtime import MTimeVersioning


class VersioningTest(TestCase):
    def setUp(self):
        self.versioning = Versioning()
        self.old_pipeline_version = settings.PIPELINE_VERSION

    def test_versioner_class(self):
        self.assertTrue(isinstance(self.versioning.versioner, MTimeVersioning))

    def test_output_filename(self):
        output_filename = self.versioning.output_filename("css/master.?.css",
            "1308127956")
        self.assertEquals(output_filename, 'css/master.0.css')

    def test_output_filename_with_version(self):
        settings.PIPELINE_VERSION = True
        output_filename = self.versioning.output_filename("css/master.?.css",
            "1308127956")
        self.assertEquals(output_filename, 'css/master.1308127956.css')

    @patch.object(MTimeVersioning, 'version')
    def test_need_update(self, mock):
        mock.return_value = "1307480052"
        need_update, version = self.versioning.need_update('css/master.1308127956.css',
            ['css/first.css'],
        )
        self.assertEquals(need_update, True)
        self.assertEquals(version, "1307480052")

    @patch.object(MTimeVersioning, 'need_update')
    def test_no_update(self, mock):
        mock.return_value = (False, "123456")
        need_update, version = self.versioning.need_update('css/master.123456.css',
            ['css/first.css'],
        )
        self.assertTrue(mock.called)
        self.assertEquals(need_update, False)
        self.assertEquals(version, "123456")

    @patch.object(MTimeVersioning, 'version')
    def test_version(self, mock):
        mock.return_value = "123456"
        version = self.versioning.version(['css/first.css'])
        self.assertTrue(mock.called)
        self.assertEquals(version, "123456")

    def test_version_from_file(self):
        settings.PIPELINE_VERSION = True
        version = self.versioning.version_from_file('css/',
            "master.?.css")
        self.assertEquals(version, "123456")

    @patch.object(storage, 'exists')
    def test_no_cleanup(self, mock):
        self.versioning.cleanup('css/master.?.css')
        self.assertFalse(mock.called)

    @patch.object(storage, 'delete')
    def test_cleanup(self, mock):
        settings.PIPELINE_VERSION = True
        self.versioning.cleanup('css/master.?.css')
        mock.assert_called_with('css/master.123456.css')

    def tearDown(self):
        settings.PIPELINE_VERSION = self.old_pipeline_version
