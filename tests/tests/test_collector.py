from __future__ import unicode_literals

import os

from django.contrib.staticfiles import finders
from django.core.files.storage import FileSystemStorage
from django.test import TestCase

from pipeline.collector import default_collector
from pipeline.finders import PipelineFinder


def local_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', path))


class CollectorTest(TestCase):
    def tearDown(self):
        super(CollectorTest, self).tearDown()

        default_collector.clear()

    def test_collect(self):
        self.assertEqual(
            set(default_collector.collect()),
            set(self._get_collectable_files()))

    def test_collect_with_files(self):
        self.assertEqual(
            set(default_collector.collect(files=[
                'pipeline/js/first.js',
                'pipeline/js/second.js',
            ])),
            set([
                'pipeline/js/first.js',
                'pipeline/js/second.js',
            ]))

    def test_delete_file_with_modified(self):
        list(default_collector.collect())

        storage = FileSystemStorage(local_path('assets'))
        new_mtime = os.path.getmtime(storage.path('js/first.js')) - 1000
        os.utime(default_collector.storage.path('pipeline/js/first.js'),
                 (new_mtime, new_mtime))

        self.assertTrue(default_collector.delete_file(
            'js/first.js', 'pipeline/js/first.js', storage))

    def test_delete_file_with_unmodified(self):
        list(default_collector.collect(files=['pipeline/js/first.js']))

        self.assertFalse(default_collector.delete_file(
            'js/first.js', 'pipeline/js/first.js',
            FileSystemStorage(local_path('assets'))))

    def _get_collectable_files(self):
        for finder in finders.get_finders():
            if not isinstance(finder, PipelineFinder):
                for path, storage in finder.list(['CVS', '.*', '*~']):
                    if getattr(storage, 'prefix', None):
                        yield os.path.join(storage.prefix, path)
                    else:
                        yield path
