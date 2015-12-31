# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pipeline.utils import guess_type, command_as_flat_list


class UtilTest(TestCase):
    def test_guess_type(self):
        self.assertEqual('text/css', guess_type('stylesheet.css'))
        self.assertEqual('text/coffeescript', guess_type('application.coffee'))
        self.assertEqual('text/less', guess_type('stylesheet.less'))


class FlatCommandAsListTest(TestCase):

    def test_command_as_string(self):
        command = 'foo bar'
        self.assertEqual(['foo bar'], command_as_flat_list(command))

    def test_command_as_list_of_string(self):
        command = ('foo', 'bar')
        self.assertEqual(['foo', 'bar'], command_as_flat_list(command))

    def test_command_as_list_with_nested_lists(self):
        command = ('foo', ('fiz', 'baz',), 'bar')
        self.assertEqual(['foo', 'fiz', 'baz', 'bar'],
                         command_as_flat_list(command))
