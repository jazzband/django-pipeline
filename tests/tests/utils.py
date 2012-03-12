# -*- coding: utf-8 -*-
from django.test import TestCase

from pipeline.utils import guess_type


class UtilTest(TestCase):
    def test_guess_type(self):
        self.assertEqual('text/css', guess_type('stylesheet.css'))
        self.assertEqual('text/coffeescript', guess_type('application.coffee'))
        self.assertEqual('text/less', guess_type('stylesheet.less'))
