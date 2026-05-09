from django.test import TestCase
from django.urls import reverse

from .models import Bosses, CurrentFight, Duties, Users


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


class BossAttackTests(TestCase):
    def test_attack_boss_uses_completed_duties_and_reports_defeat(self):
        user = Users.objects.create(
            username="fighter",
            password="secret",
            user_class="Knight",
        )
        boss = Bosses.objects.create(
            boss_hp=6,
            weakness="focus",
            boss_name="Deadline Drake",
        )
        CurrentFight.objects.create(user_id=user, boss_id=boss, seconds_left=300)
        Duties.objects.create(
            user_id=user,
            description="finish report",
            strength=2,
            intelligence=3,
            charisma=1,
            status="Completed",
        )
        Duties.objects.create(
            user_id=user,
            description="still pending",
            strength=99,
            intelligence=99,
            charisma=99,
            status="Active",
        )
        session = self.client.session
        session["user_id"] = user.user_id
        session.save()

        response = self.client.post(
            reverse("attack_boss"),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["attack_damage"], 6)
        self.assertEqual(response.json()["boss_hp"], 0)
        self.assertTrue(response.json()["boss_defeated"])

        boss.refresh_from_db()
        self.assertEqual(boss.boss_hp, 0)
        self.assertEqual(
            Duties.objects.get(description="finish report").status,
            "Used",
        )
        self.assertEqual(
            Duties.objects.get(description="still pending").status,
            "Active",
        )
