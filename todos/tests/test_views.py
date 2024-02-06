from django.test import TestCase
from django.urls import reverse

from todos.forms import TodoItemForm
from todos.models import TodoItem


class TodoItemListViewTests(TestCase):
    def test_get(self):
        response = self.client.get(reverse("todos:todoitem-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        self.assertIsInstance(response.context_data["form"], TodoItemForm)

    def test_get_with_htmx(self):
        response = self.client.get(
            reverse("todos:todoitem-list"), headers={"hx-request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No todo items found.")
        self.assertNotContains(response, "form")


class TodoItemCreateViewTests(TestCase):
    def test_get_is_allowed(self):
        response = self.client.get(reverse("todos:todoitem-create"))
        self.assertEqual(response.status_code, 405)

    def test_post_with_validation_error(self):
        response = self.client.post(
            reverse("todos:todoitem-create"),
            {"description": "Test description"},
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        self.assertContains(response, "This field is required.")
        self.assertEqual(response.headers["HX-Retarget"], "this")

    def test_post_success(self):
        response = self.client.post(
            reverse("todos:todoitem-create"),
            {"title": "Test description"},
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("todos:todoitem-list"))
        self.assertEqual(TodoItem.objects.count(), 1)


class TodoItemDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = TodoItem.objects.create(title="Test description")

    def test_get_not_allowed(self):
        response = self.client.get(
            reverse("todos:todoitem-delete", args=[self.item.id])
        )
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        response = self.client.post(
            reverse("todos:todoitem-delete", args=[self.item.id]),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("todos:todoitem-list"))
        self.assertEqual(TodoItem.objects.count(), 0)


class TodoMarkCompleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = TodoItem.objects.create(title="Test description")

    def test_get_not_allowed(self):
        response = self.client.get(
            reverse("todos:todoitem-mark-complete", args=[self.item.id])
        )
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        response = self.client.post(
            reverse("todos:todoitem-mark-complete", args=[self.item.id]),
            headers={"hx-request": "true"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("todos:todoitem-list"))
        self.item.refresh_from_db()
        self.assertIsNotNone(self.item.completed_on)
