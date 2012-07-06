# -*- coding: utf-8 -*-
from django.test import TestCase

from pipeline.utils import guess_type, template_name


class UtilTest(TestCase):
    def test_guess_type(self):
        self.assertEqual('text/css', guess_type('stylesheet.css'))
        self.assertEqual('text/coffeescript', guess_type('application.coffee'))
        self.assertEqual('text/less', guess_type('stylesheet.less'))

    def test_template_name(self):
        name = template_name('templates/photo/detail.jst',
            'templates/')
        self.assertEquals(name, 'photo_detail')
        name = template_name('templates/photo_edit.jst', '')
        self.assertEquals(name, 'photo_edit')
        name = template_name('templates\photo\detail.jst',
            'templates\\')
        self.assertEquals(name, 'photo_detail')
