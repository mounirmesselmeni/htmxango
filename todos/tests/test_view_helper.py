from pathlib import Path

from django.test import RequestFactory, TestCase, override_settings

from todos.views import HtmxResponseClass


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [Path(__file__).resolve().parent / "templates"],
        }
    ]
)
class HtmxResponseClassTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.template = "test.tpl.html"

    def test_rendered_content_with_htmx(self):
        request = self.factory.get("/")
        request.htmx = True
        response = HtmxResponseClass(
            htmx_template_block="main_block",
            template=self.template,
            context={"data": "Hello, World!"},
            request=request,
        )
        rendered_content = response.rendered_content
        self.assertTrue("Hello, World!" in rendered_content)
        self.assertTrue("Rendered content with htmx" in rendered_content)

    def test_rendered_content_without_htmx(self):
        request = self.factory.get("/")
        request.htmx = False
        response = HtmxResponseClass(
            template=self.template,
            context={"data": "Hello, World!"},
            request=request,
        )
        rendered_content = response.rendered_content
        self.assertTrue("Hello, World!" in rendered_content)
        self.assertTrue("Rendered content without htmx" in rendered_content)
        self.assertTrue("Rendered content with htmx" in rendered_content)
