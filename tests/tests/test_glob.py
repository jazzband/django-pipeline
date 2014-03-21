from __future__ import unicode_literals

import os
import shutil

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.test import TestCase

from pipeline import glob

local_path = lambda path: os.path.join(os.path.dirname(__file__), path)


class GlobTest(TestCase):
    def normpath(self, *parts):
        return os.path.normpath(os.path.join(*parts))

    def mktemp(self, *parts):
        filename = self.normpath(*parts)
        base, file = os.path.split(filename)
        base = os.path.join(self.storage.location, base)
        if not os.path.exists(base):
            os.makedirs(base)
        self.storage.save(filename, ContentFile(""))

    def assertSequenceEqual(self, l1, l2):
        self.assertEqual(set(l1), set(l2))

    def setUp(self):
        self.storage = FileSystemStorage(local_path('glob_dir'))
        self.old_storage = glob.staticfiles_storage
        glob.staticfiles_storage = self.storage
        self.mktemp('a', 'D')
        self.mktemp('aab', 'F')
        self.mktemp('aaa', 'zzzF')
        self.mktemp('ZZZ')
        self.mktemp('a', 'bcd', 'EF')
        self.mktemp('a', 'bcd', 'efg', 'ha')

    def glob(self, *parts):
        if len(parts) == 1:
            pattern = parts[0]
        else:
            pattern = os.path.join(*parts)
        return glob.glob(pattern)

    def tearDown(self):
        shutil.rmtree(self.storage.location)
        glob.staticfiles_storage = self.old_storage

    def test_glob_literal(self):
        self.assertSequenceEqual(self.glob('a'),
            [self.normpath('a')])
        self.assertSequenceEqual(self.glob('a', 'D'),
            [self.normpath('a', 'D')])
        self.assertSequenceEqual(self.glob('aab'),
            [self.normpath('aab')])
        self.assertSequenceEqual(self.glob('zymurgy'), [])

    def test_glob_one_directory(self):
        self.assertSequenceEqual(self.glob('a*'),
            map(self.normpath, ['a', 'aab', 'aaa']))
        self.assertSequenceEqual(self.glob('*a'),
            map(self.normpath, ['a', 'aaa']))
        self.assertSequenceEqual(self.glob('aa?'),
            map(self.normpath, ['aaa', 'aab']))
        self.assertSequenceEqual(self.glob('aa[ab]'),
            map(self.normpath, ['aaa', 'aab']))
        self.assertSequenceEqual(self.glob('*q'), [])

    def test_glob_nested_directory(self):
        if os.path.normcase("abCD") == "abCD":
            # case-sensitive filesystem
            self.assertSequenceEqual(self.glob('a', 'bcd', 'E*'),
                [self.normpath('a', 'bcd', 'EF')])
        else:
            # case insensitive filesystem
            self.assertSequenceEqual(self.glob('a', 'bcd', 'E*'), [
                self.normpath('a', 'bcd', 'EF'),
                self.normpath('a', 'bcd', 'efg')
            ])
        self.assertSequenceEqual(self.glob('a', 'bcd', '*g'),
            [self.normpath('a', 'bcd', 'efg')])

    def test_glob_directory_names(self):
        self.assertSequenceEqual(self.glob('*', 'D'),
            [self.normpath('a', 'D')])
        self.assertSequenceEqual(self.glob('*', '*a'), [])
        self.assertSequenceEqual(self.glob('a', '*', '*', '*a'),
           [self.normpath('a', 'bcd', 'efg', 'ha')])
        self.assertSequenceEqual(self.glob('?a?', '*F'),
            map(self.normpath, [os.path.join('aaa', 'zzzF'),
            os.path.join('aab', 'F')]))

    def test_glob_directory_with_trailing_slash(self):
        # We are verifying that when there is wildcard pattern which
        # ends with os.sep doesn't blow up.
        paths = glob.glob('*' + os.sep)
        self.assertEqual(len(paths), 4)
        self.assertTrue(all([os.sep in path for path in paths]))
