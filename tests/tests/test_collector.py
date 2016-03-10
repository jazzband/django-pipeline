from __future__ import unicode_literals

import os

from django.contrib.staticfiles import finders
from django.test import TestCase

from pipeline.collector import default_collector
from pipeline.finders import PipelineFinder


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

    def _get_collectable_files(self):
        for finder in finders.get_finders():
            if not isinstance(finder, PipelineFinder):
                for path, storage in finder.list(['CVS', '.*', '*~']):
                    if getattr(storage, 'prefix', None):
                        yield os.path.join(storage.prefix, path)
                    else:
                        yield path
