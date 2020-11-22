import copy
from unittest.mock import patch

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from jinja2 import Environment, PackageLoader

from django.template import Template, Context
from django.test import TestCase

from pipeline.jinja2 import PipelineExtension

from tests.utils import pipeline_settings


class JinjaTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        staticfiles_storage._setup()
        call_command('collectstatic', verbosity=0, interactive=False)

    def setUp(self):
        self.env = Environment(extensions=[PipelineExtension],
                               loader=PackageLoader('pipeline', 'templates'))

    def test_no_package(self):
        template = self.env.from_string(u"""{% stylesheet "unknow" %}""")
        self.assertEqual(u'', template.render())
        template = self.env.from_string(u"""{% javascript "unknow" %}""")
        self.assertEqual(u'', template.render())

    def test_package_css(self):
        template = self.env.from_string(u"""{% stylesheet "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" />', template.render())

    @pipeline_settings(PIPELINE_ENABLED=False)
    def test_package_css_disabled(self):
        template = self.env.from_string(u"""{% stylesheet "screen" %}""")
        self.assertEqual(u'''<link href="/static/pipeline/css/first.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/second.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/urls.css" rel="stylesheet" type="text/css" />''', template.render())

    def test_package_js(self):
        template = self.env.from_string(u"""{% javascript "scripts" %}""")
        self.assertEqual(u'<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>', template.render())

    def test_package_js_async(self):
        template = self.env.from_string(u"""{% javascript "scripts_async" %}""")
        self.assertEqual(u'<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>', template.render())

    def test_package_js_defer(self):
        template = self.env.from_string(u"""{% javascript "scripts_defer" %}""")
        self.assertEqual(u'<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>', template.render())

    def test_package_js_async_defer(self):
        template = self.env.from_string(u"""{% javascript "scripts_async_defer" %}""")
        self.assertEqual(u'<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>', template.render())

    def test_crossorigin(self):
        template = self.env.from_string("""{% javascript "scripts_crossorigin" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_crossorigin.js" charset="utf-8" crossorigin="anonymous"></script>', template.render())

    def test_sri_sha256(self):
        template = self.env.from_string("""{% javascript "scripts_sri_sha256" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha256.js" charset="utf-8" integrity="sha256-sO+6B+wKBraSBcdPSa3kkvmFKTmwk0vHUik+t4j2gcM="></script>', template.render())

    def test_sri_sha384(self):
        template = self.env.from_string("""{% javascript "scripts_sri_sha384" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha384.js" charset="utf-8" integrity="sha384-qaJwWufiQ3S+T22m9nG6NuUfXwuaqC056iKaXozyyB+9Jf4dhFIoujkDskHSMTsw"></script>', template.render())

    def test_sri_sha512(self):
        template = self.env.from_string("""{% javascript "scripts_sri_sha512" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha512.js" charset="utf-8" integrity="sha512-YYPVp/KIfwuwsWUDqsrevzsx+YbXAeGVUVH3SDDAAByNlVnptKDCnM+9ECVriVFK2R2dTvBE9Bpy1oBQCvU4RA=="></script>', template.render())


class DjangoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        staticfiles_storage._setup()
        call_command('collectstatic', verbosity=0, interactive=False)

    def render_template(self, template):
        return Template(template).render(Context())

    def test_compressed_empty(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "unknow" %}""")
        self.assertEqual(u'', rendered)

    def test_compressed_css(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" media="all" />', rendered)

    def test_compressed_css_media(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen_media" %}""")
        self.assertEqual(u'<link href="/static/screen_media.css" rel="stylesheet" type="text/css" media="screen and (min-width:500px)" />', rendered)

    def test_compressed_css_title(self):
        rendered = self.render_template(u"""{% load pipeline %}{% stylesheet "screen_title" %}""")
        self.assertEqual(u'<link href="/static/screen_title.css" rel="stylesheet" type="text/css" media="all" title="Default Style" />', rendered)

    def test_compressed_js(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts" %}""")
        self.assertEqual(u'<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_async(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_async" %}""")
        self.assertEqual(u'<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_defer(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_defer" %}""")
        self.assertEqual(u'<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>', rendered)

    def test_compressed_js_async_defer(self):
        rendered = self.render_template(u"""{% load pipeline %}{% javascript "scripts_async_defer" %}""")
        self.assertEqual(u'<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>', rendered)

    def test_crossorigin(self):
        rendered = self.render_template("""{% load pipeline %}{% javascript "scripts_crossorigin" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_crossorigin.js" charset="utf-8" crossorigin="anonymous"></script>', rendered)

    def test_sri_sha256(self):
        rendered = self.render_template("""{% load pipeline %}{% javascript "scripts_sri_sha256" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha256.js" charset="utf-8" integrity="sha256-sO+6B+wKBraSBcdPSa3kkvmFKTmwk0vHUik+t4j2gcM="></script>', rendered)

    def test_sri_sha384(self):
        staticfiles_storage._setup()
        call_command('collectstatic', verbosity=0, interactive=False)
        rendered = self.render_template("""{% load pipeline %}{% javascript "scripts_sri_sha384" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha384.js" charset="utf-8" integrity="sha384-qaJwWufiQ3S+T22m9nG6NuUfXwuaqC056iKaXozyyB+9Jf4dhFIoujkDskHSMTsw"></script>', rendered)

    def test_sri_sha512(self):
        staticfiles_storage._setup()
        call_command('collectstatic', verbosity=0, interactive=False)
        rendered = self.render_template("""{% load pipeline %}{% javascript "scripts_sri_sha512" %}""")
        self.assertEqual('<script type="text/javascript" src="/static/scripts_sha512.js" charset="utf-8" integrity="sha512-YYPVp/KIfwuwsWUDqsrevzsx+YbXAeGVUVH3SDDAAByNlVnptKDCnM+9ECVriVFK2R2dTvBE9Bpy1oBQCvU4RA=="></script>', rendered)
