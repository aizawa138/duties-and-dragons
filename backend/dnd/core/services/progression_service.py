EXP_PER_LEVEL = 10
BOSS_HP_PER_LEVEL = 10


def calculate_user_exp(user):
    return user.strength + user.inteligence + user.charisma


def calculate_user_level(exp):
    return int(exp // EXP_PER_LEVEL)


def update_user_progression(user):
    user.exp = calculate_user_exp(user)
    user.level = calculate_user_level(user.exp)
    return user


def save_user_progression(user):
    previous_exp = user.exp
    previous_level = user.level
    update_user_progression(user)

    if user.exp != previous_exp or user.level != previous_level:
        user.save(update_fields=["exp", "level"])

    return user


def add_stats_to_user(user, strength=0, intelligence=0, charisma=0):
    user.strength += strength
    user.inteligence += intelligence
    user.charisma += charisma
    update_user_progression(user)
    user.save(
        update_fields=[
            "strength",
            "inteligence",
            "charisma",
            "exp",
            "level",
        ]
    )
    return user


def get_scaled_boss_hp(base_hp, user):
    level = calculate_user_level(calculate_user_exp(user))
    return int((base_hp or 0) + (level * BOSS_HP_PER_LEVEL))
