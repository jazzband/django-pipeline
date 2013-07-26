from __future__ import with_statement

import os
import sys
import unittest
from os.path import join as pjoin

from pipeline.html_utils import minify_html_leave_whitespace

DIR = os.path.abspath(os.path.dirname(__file__))


class HtmlUtilsTestCase(unittest.TestCase):
    def test_minify_html_leave_whitespace(self):
        files = [
            ('html1_actual.html', 'html1_expected.html')
        ]

        for actual, expected, in files:
            file_path_actual = pjoin(DIR, 'assets/html/', actual)
            file_path_expected = pjoin(DIR, 'assets/html/', expected)

            with open(file_path_actual, 'r') as fp:
                content_actual = fp.read().strip()

            with open(file_path_expected, 'r') as fp:
                content_expected = fp.read().strip()

            result = minify_html_leave_whitespace(content_actual)
            self.assertEqual(result, content_expected)


if __name__ == '__main__':
    sys.exit(unittest.main())
