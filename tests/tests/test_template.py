from django.template import Context, Template
from django.test import TestCase
from jinja2 import Environment, PackageLoader

from pipeline.jinja2 import PipelineExtension
from tests.utils import pipeline_settings


class JinjaTest(TestCase):
    def setUp(self):
        self.env = Environment(
            extensions=[PipelineExtension],
            loader=PackageLoader("pipeline", "templates"),
        )

    def test_no_package(self):
        template = self.env.from_string("""{% stylesheet "unknow" %}""")
        self.assertEqual("", template.render())
        template = self.env.from_string("""{% javascript "unknow" %}""")
        self.assertEqual("", template.render())

    def test_package_css(self):
        template = self.env.from_string("""{% stylesheet "screen" %}""")
        self.assertEqual(
            '<link href="/static/screen.css" rel="stylesheet" type="text/css" />',
            template.render(),
        )

    @pipeline_settings(PIPELINE_ENABLED=False)
    def test_package_css_disabled(self):
        template = self.env.from_string("""{% stylesheet "screen" %}""")
        self.assertEqual(
            """<link href="/static/pipeline/css/first.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/second.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/urls.css" rel="stylesheet" type="text/css" />""",  # noqa
            template.render(),
        )

    def test_package_js(self):
        template = self.env.from_string("""{% javascript "scripts" %}""")
        self.assertEqual(
            '<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>',  # noqa
            template.render(),
        )

    def test_package_js_async(self):
        template = self.env.from_string("""{% javascript "scripts_async" %}""")
        self.assertEqual(
            '<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>',  # noqa
            template.render(),
        )

    def test_package_js_defer(self):
        template = self.env.from_string("""{% javascript "scripts_defer" %}""")
        self.assertEqual(
            '<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>',  # noqa
            template.render(),
        )

    def test_package_js_async_defer(self):
        template = self.env.from_string("""{% javascript "scripts_async_defer" %}""")
        self.assertEqual(
            '<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>',  # noqa
            template.render(),
        )


class DjangoTest(TestCase):
    def render_template(self, template):
        return Template(template).render(Context())

    def test_compressed_empty(self):
        rendered = self.render_template(
            """{% load pipeline %}{% stylesheet "unknow" %}""",
        )
        self.assertEqual("", rendered)

    def test_compressed_css(self):
        rendered = self.render_template(
            """{% load pipeline %}{% stylesheet "screen" %}""",
        )
        self.assertEqual(
            '<link href="/static/screen.css" rel="stylesheet" type="text/css" media="all" />',  # noqa
            rendered,
        )

    def test_compressed_css_media(self):
        rendered = self.render_template(
            """{% load pipeline %}{% stylesheet "screen_media" %}""",
        )
        self.assertEqual(
            '<link href="/static/screen_media.css" rel="stylesheet" type="text/css" media="screen and (min-width:500px)" />',  # noqa
            rendered,
        )

    def test_compressed_css_title(self):
        rendered = self.render_template(
            """{% load pipeline %}{% stylesheet "screen_title" %}""",
        )
        self.assertEqual(
            '<link href="/static/screen_title.css" rel="stylesheet" type="text/css" media="all" title="Default Style" />',  # noqa
            rendered,
        )

    def test_compressed_js(self):
        rendered = self.render_template(
            """{% load pipeline %}{% javascript "scripts" %}""",
        )
        self.assertEqual(
            '<script type="text/javascript" src="/static/scripts.js" charset="utf-8"></script>',  # noqa
            rendered,
        )

    def test_compressed_js_async(self):
        rendered = self.render_template(
            """{% load pipeline %}{% javascript "scripts_async" %}""",
        )
        self.assertEqual(
            '<script async type="text/javascript" src="/static/scripts_async.js" charset="utf-8"></script>',  # noqa
            rendered,
        )

    def test_compressed_js_defer(self):
        rendered = self.render_template(
            """{% load pipeline %}{% javascript "scripts_defer" %}""",
        )
        self.assertEqual(
            '<script defer type="text/javascript" src="/static/scripts_defer.js" charset="utf-8"></script>',  # noqa
            rendered,
        )

    def test_compressed_js_async_defer(self):
        rendered = self.render_template(
            """{% load pipeline %}{% javascript "scripts_async_defer" %}""",
        )
        self.assertEqual(
            '<script async defer type="text/javascript" src="/static/scripts_async_defer.js" charset="utf-8"></script>',  # noqa
            rendered,
        )
