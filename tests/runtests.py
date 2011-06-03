#!/usr/bin/env python
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
            'tests',
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
    sys.path.insert(0, os.path.join(TEST_DIR, ".."))
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
