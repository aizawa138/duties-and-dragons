from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Bosses, CurrentFight, Duties, Habits, Users
from .services.fight_service import ensure_current_fight
from .services.progression_service import (
    calculate_user_exp,
    calculate_user_level,
    get_scaled_boss_hp,
)


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
            boss_hp=10,
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
        Habits.objects.create(
            user_id=user,
            description="daily practice",
            strength=1,
            intelligence=1,
            charisma=2,
            status="Completed",
        )
        session = self.client.session
        session["user_id"] = user.user_id
        session.save()

        response = self.client.post(
            reverse("attack_boss"),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["attack_damage"], 10)
        self.assertEqual(response.json()["boss_hp"], 0)
        self.assertTrue(response.json()["boss_defeated"])

        current_fight = CurrentFight.objects.get(user_id=user)
        self.assertEqual(current_fight.current_boss_hp, 0)
        user.refresh_from_db()
        self.assertEqual(user.strength, 3)
        self.assertEqual(user.inteligence, 4)
        self.assertEqual(user.charisma, 3)
        self.assertEqual(user.exp, 10)
        self.assertEqual(user.level, 1)
        self.assertEqual(
            Duties.objects.get(description="finish report").status,
            "Used",
        )
        self.assertEqual(
            Duties.objects.get(description="still pending").status,
            "Active",
        )
        self.assertEqual(
            Habits.objects.get(description="daily practice").status,
            "Used",
        )


class FightRotationTests(TestCase):
    def test_expired_fight_rotates_to_next_boss_with_new_weekly_timer(self):
        user = Users.objects.create(
            username="weekly-fighter",
            password="secret",
            user_class="Knight",
        )
        boss_1 = Bosses.objects.create(
            boss_id=1,
            boss_hp=10,
            weakness="strength",
            boss_name="Boss One",
        )
        boss_2 = Bosses.objects.create(
            boss_id=2,
            boss_hp=20,
            weakness="intelligence",
            boss_name="Boss Two",
        )
        Bosses.objects.create(
            boss_id=3,
            boss_hp=30,
            weakness="charisma",
            boss_name="Boss Three",
        )
        expired_fight = CurrentFight.objects.create(
            user_id=user,
            boss_id=boss_1,
            current_boss_hp=3,
            seconds_left=0,
            started_at=timezone.now() - timezone.timedelta(days=8),
            ends_at=timezone.now() - timezone.timedelta(seconds=1),
        )

        current_fight = ensure_current_fight(user)

        self.assertNotEqual(current_fight.fight_id, expired_fight.fight_id)
        self.assertEqual(current_fight.boss_id, boss_2)
        self.assertEqual(current_fight.current_boss_hp, boss_2.boss_hp)
        self.assertGreater(current_fight.seconds_left, 0)


class ProgressionTests(TestCase):
    def test_exp_level_and_boss_hp_scaling_are_based_on_user_stats(self):
        user = Users.objects.create(
            username="scaler",
            password="secret",
            user_class="Knight",
            strength=12,
            inteligence=8,
            charisma=5,
        )

        self.assertEqual(calculate_user_exp(user), 25)
        self.assertEqual(calculate_user_level(calculate_user_exp(user)), 2)

        user.exp = calculate_user_exp(user)
        user.level = calculate_user_level(user.exp)

        self.assertEqual(get_scaled_boss_hp(100, user), 120)
