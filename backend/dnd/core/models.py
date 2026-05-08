from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    # Stats
    strength = models.FloatField()
    inteligence = models.FloatField()
    charisma = models.FloatField()
    exp = models.FloatField()
    level = models.IntegerField()
    user_class = models.CharField(max_length=64)
    user_hp = models.IntegerField()


class Bosses(models.Model):
    boss_id = models.AutoField(primary_key=True)
    boss_hp = models.IntegerField()
    weakness = models.CharField()
    boss_name = models.CharField()


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
    seconds_left = models.IntegerField()


class Duties(models.Model):
    duty_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="duties", blank=False
    )
    description = models.CharField(max_length=7000)
    strength = models.FloatField(default=0.0)
    intelligence = models.FloatField(default=0.0)
    charisma = models.FloatField(default=0.0)
