from datetime import timedelta
from math import ceil

from django.db import transaction
from django.utils import timezone

from ..models import Bosses, CurrentFight


BOSS_ROTATION_IDS = (1, 2, 3)
FIGHT_DURATION = timedelta(days=7)
FIGHT_DURATION_SECONDS = int(FIGHT_DURATION.total_seconds())


def get_fight_ends_at(started_at=None):
    return (started_at or timezone.now()) + FIGHT_DURATION


def get_seconds_left(fight, now=None):
    now = now or timezone.now()
    return max(0, ceil((fight.ends_at - now).total_seconds()))


def get_next_boss_id(current_boss_id):
    if current_boss_id not in BOSS_ROTATION_IDS:
        return BOSS_ROTATION_IDS[0]

    current_index = BOSS_ROTATION_IDS.index(current_boss_id)
    next_index = (current_index + 1) % len(BOSS_ROTATION_IDS)
    return BOSS_ROTATION_IDS[next_index]


def get_boss_for_rotation(boss_id):
    return Bosses.objects.get(boss_id=boss_id)


def create_current_fight(user, boss=None, now=None):
    now = now or timezone.now()
    boss = boss or get_boss_for_rotation(BOSS_ROTATION_IDS[0])

    return CurrentFight.objects.create(
        user_id=user,
        boss_id=boss,
        current_boss_hp=boss.boss_hp,
        seconds_left=FIGHT_DURATION_SECONDS,
        started_at=now,
        ends_at=get_fight_ends_at(now),
    )


def reset_current_fight(current_fight, boss, now=None):
    now = now or timezone.now()

    current_fight.boss_id = boss
    current_fight.current_boss_hp = boss.boss_hp
    current_fight.seconds_left = FIGHT_DURATION_SECONDS
    current_fight.started_at = now
    current_fight.ends_at = get_fight_ends_at(now)
    current_fight.save(
        update_fields=[
            "boss_id",
            "current_boss_hp",
            "seconds_left",
            "started_at",
            "ends_at",
        ]
    )
    return current_fight


@transaction.atomic
def rotate_fight(current_fight, now=None):
    now = now or timezone.now()
    user = current_fight.user_id
    next_boss = get_boss_for_rotation(get_next_boss_id(current_fight.boss_id_id))

    current_fight.delete()
    return create_current_fight(user=user, boss=next_boss, now=now)


def ensure_current_fight(user, now=None):
    now = now or timezone.now()
    current_fight = (
        CurrentFight.objects.select_related("boss_id")
        .filter(user_id=user)
        .first()
    )

    if not current_fight:
        return create_current_fight(user=user, now=now)

    if current_fight.ends_at <= now:
        return rotate_fight(current_fight, now=now)

    seconds_left = get_seconds_left(current_fight, now=now)
    if current_fight.seconds_left != seconds_left:
        current_fight.seconds_left = seconds_left
        current_fight.save(update_fields=["seconds_left"])

    return current_fight


def rotate_expired_fights(now=None):
    now = now or timezone.now()
    expired_fights = (
        CurrentFight.objects.select_related("user_id", "boss_id")
        .filter(ends_at__lte=now)
    )

    for current_fight in expired_fights:
        try:
            rotate_fight(current_fight, now=now)
        except Bosses.DoesNotExist:
            continue


def serialize_current_fight(current_fight, now=None):
    now = now or timezone.now()
    return {
        "fight_id": current_fight.fight_id,
        "boss_id": current_fight.boss_id_id,
        "boss_name": current_fight.boss_id.boss_name,
        "boss_hp": current_fight.current_boss_hp,
        "seconds_left": get_seconds_left(current_fight, now=now),
        "started_at": current_fight.started_at,
        "ends_at": current_fight.ends_at,
    }
