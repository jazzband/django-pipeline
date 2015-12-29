# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pipeline.conf import PipelineSettings


class TestSettings(TestCase):
    def test_3unicode(self):
        s = PipelineSettings({"FOO_BINARY": "env actualprogram"})
        self.assertEqual(s.FOO_BINARY, ('env', 'actualprogram'))

    def test_2unicode(self):
        s = PipelineSettings({"FOO_BINARY": u"env actualprogram"})
        self.assertEqual(s.FOO_BINARY, ('env', 'actualprogram'))

    def test_2bytes(self):
        s = PipelineSettings({"FOO_BINARY": "env actualprogram"})
        self.assertEqual(s.FOO_BINARY, ('env', 'actualprogram'))

    def test_expected_splitting(self):
        s = PipelineSettings({"FOO_BINARY": "env actualprogram"})
        self.assertEqual(s.FOO_BINARY, ('env', 'actualprogram'))

    def test_expected_preservation(self):
        s = PipelineSettings({"FOO_BINARY": r"actual\ program"})
        self.assertEqual(s.FOO_BINARY, ('actual program',))

    def test_tuples_are_normal(self):
        s = PipelineSettings({"FOO_ARGUMENTS": ("explicit", "with", "args")})
        self.assertEqual(s.FOO_ARGUMENTS, ('explicit', 'with', 'args'))
