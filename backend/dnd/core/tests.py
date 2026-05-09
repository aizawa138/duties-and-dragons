from django.test import TestCase
from django.urls import reverse

from .models import Users


class AuthFlowTests(TestCase):
    def test_register_authenticates_new_user_for_class_selection(self):
        response = self.client.post(
            reverse("register_user"),
            {"username": "new-user", "password": "secret-password"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", self.client.session)

        response = self.client.post(
            reverse("choose_class"),
            {"user_class": "Knight"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        user = Users.objects.get(username="new-user")
        self.assertEqual(user.user_class, "Knight")
        self.assertEqual(user.strength, 2)
        self.assertEqual(user.inteligence, 1)
        self.assertEqual(user.charisma, 1)

    def test_choose_class_requires_session_user(self):
        response = self.client.post(
            reverse("choose_class"),
            {"user_class": "Knight"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
