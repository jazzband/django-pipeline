#!/usr/bin/env python
import coverage
import os
import sys

from django.conf import settings

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        PIPELINE_CACHE_BACKEND='dummy://',
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=[
            'pipeline',
            'tests'
        ],
        MEDIA_URL='/media/',
        MEDIA_ROOT=os.path.join(TEST_DIR, 'media/'),
        STATIC_URL='/static/',
        STATIC_ROOT=os.path.join(TEST_DIR, 'static/'),
        TEMPLATE_DIRS=(
            os.path.join(TEST_DIR, 'templates'),
        ),
        TEST_DIR=TEST_DIR,
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['tests']
    parent_dir = os.path.join(TEST_DIR, "../")
    sys.path.insert(0, parent_dir)
    cover = coverage.coverage(branch=True, cover_pylib=False,
        include=[
            os.path.join(parent_dir, 'pipeline', '*.py')
        ],
        omit=[
            os.path.join(parent_dir, 'tests', '*.py'),
            os.path.join(parent_dir, 'pipeline', 'compressors',
                'jsmin', 'jsmin.py'),
        ]
    )
    cover.load()
    cover.start()
    failures = run_tests(test_args, verbosity=1, interactive=True)
    cover.stop()
    cover.save()
    cover.report(file=sys.stdout)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
