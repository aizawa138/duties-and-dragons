from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone


def default_fight_ends_at():
    return timezone.now() + timezone.timedelta(days=7)


# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, default=None, blank=False)
    password = models.CharField(max_length=128, default=None)
    # Stats
    strength = models.FloatField(default=0.0)
    inteligence = models.FloatField(default=0.0)
    charisma = models.FloatField(default=0.0)
    exp = models.FloatField(default=0.0)
    level = models.IntegerField(default=0)
    user_class = models.CharField(max_length=64)
    user_hp = models.IntegerField(default=100)


class Bosses(models.Model):
    boss_id = models.AutoField(primary_key=True)
    boss_hp = models.IntegerField(default=None)
    weakness = models.CharField(max_length=100, default=None)
    boss_name = models.CharField(max_length=100, default=None)


class CurrentFight(models.Model):
    fight_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        related_name="currentFight",
        blank=False,
        null=False,
    )
    boss_id = models.ForeignKey(
        "Bosses",
        on_delete=models.CASCADE,
        related_name="currentFight",
        blank=False,
        null=False,
    )
    seconds_left = models.IntegerField(default=None)
    current_boss_hp = models.IntegerField(default=None)
    started_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(default=default_fight_ends_at)


class Duties(models.Model):
    duty_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="duties", blank=False
    )
    description = models.CharField(max_length=7000, default=None)
    strength = models.FloatField(default=0.0)
    intelligence = models.FloatField(default=0.0)
    charisma = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=64, default="Active"
    )  # Active, Completed, Used
    deadline = models.DateField(default=timezone.localdate)


class Habits(models.Model):
    habit_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="habits", blank=False
    )
    description = models.CharField(max_length=7000, default=None)
    strength = models.FloatField(default=0.0)
    intelligence = models.FloatField(default=0.0)
    charisma = models.FloatField(default=0.0)
    status = models.CharField(max_length=64, default="Active")  # Active, Completed


class DailyResetState(models.Model):
    key = models.CharField(max_length=128, unique=True)
    last_reset_date = models.DateField()

