from django.shortcuts import render
from functools import wraps
from math import ceil

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .models import Users, Bosses, CurrentFight, Duties, Habits
import os

# AI import
from google import genai

# api for stats
from .services.ai_service import generate_task_rewards
from .services.fight_service import (
    create_current_fight,
    ensure_current_fight,
    reset_current_fight,
    serialize_current_fight,
)


def _get_task_rewards(user_id, task_description):
    """Helper function to get task rewards for a user"""
    try:
        user = Users.objects.get(user_id=user_id)
        current_fight = ensure_current_fight(user)
        boss_max_hp = current_fight.boss_id.boss_hp
    except (Users.DoesNotExist, Bosses.DoesNotExist):
        raise ValueError("No current fight")

    if not task_description:
        raise ValueError("task_description is required")

    try:
        rewards = generate_task_rewards(task_description, boss_max_hp)
    except ValueError as exc:
        raise ValueError(str(exc))

    return rewards


def _is_boss_defeated(boss_hp):
    return boss_hp <= 0


def _populate_completed_stats(user):
    """Attach completed stat totals from duties and habits onto the user."""
    completed_duties = Duties.objects.filter(user_id=user, status="Completed")
    completed_habits = Habits.objects.filter(user_id=user, status="Completed")

    total_strength = (
        completed_duties.aggregate(Sum("strength"))["strength__sum"] or 0
    ) + (
        completed_habits.aggregate(Sum("strength"))["strength__sum"] or 0
    )
    total_intelligence = (
        completed_duties.aggregate(Sum("intelligence"))["intelligence__sum"] or 0
    ) + (
        completed_habits.aggregate(Sum("intelligence"))["intelligence__sum"] or 0
    )
    total_charisma = (
        completed_duties.aggregate(Sum("charisma"))["charisma__sum"] or 0
    ) + (
        completed_habits.aggregate(Sum("charisma"))["charisma__sum"] or 0
    )

    user.total_strength = total_strength
    user.total_intelligence = total_intelligence
    user.total_charisma = total_charisma

    return user


# Custom authentication decorator for custom Users model
def custom_auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")
        if not user_id:
            return Response({"error": "Unauthorized1"}, status=401)
        try:
            request.custom_user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "Unauthorized2"}, status=401)
        return func(request, *args, **kwargs)

    return wrapper


CLASS_STARTING_STATS = {
    "Knight": {
        "strength": 2,
        "inteligence": 1,
        "charisma": 1,
        "user_hp": 100,
    },
    "Mage": {
        "strength": 1,
        "inteligence": 2,
        "charisma": 1,
        "user_hp": 100,
    },
    "Vampire": {
        "strength": 1,
        "inteligence": 1,
        "charisma": 2,
        "user_hp": 100,
    },
}

CLASS_ALIASES = {
    "Berserker": "Knight",
}


@ensure_csrf_cookie
def set_csrf_token(request):
    """
    This view sets the CSRF cookie in the user's browser.
    """
    return JsonResponse(
        {"details": "CSRF cookie set", "csrfToken": get_token(request)},
        status=200,
    )


@api_view(["POST"])
def register_user(request):
    data = request.data

    username = data.get("username")  # test fail case
    password = data.get("password")

    # check missing fields
    if not username or not password:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    # check duplicate username
    if Users.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # create user with default class
    user = Users.objects.create(
        username=username,
        password=make_password(password),
        user_class="",  # Default empty class until user selects one
    )
    user.save()

    # Keep signup and login behavior aligned so authenticated setup pages work.
    request.session["user_id"] = user.user_id
    request.session.save()

    boss_id = 1

    if CurrentFight.objects.filter(user_id=user.user_id).exists():
        return Response({"error": "Already in a fight"}, status=400)

    try:
        boss = Bosses.objects.get(boss_id=boss_id)
    except Bosses.DoesNotExist:
        return Response({"error": "Boss not found"}, status=404)

    current_fight = create_current_fight(user=user, boss=boss)

    return Response(
        {
            "message": "Fight started",
            "fight_id": current_fight.fight_id,
            "boss_id": boss.boss_id,
            "boss_name": boss.boss_name,
            "base_boss_hp": boss.boss_hp,
            "boss_hp": current_fight.current_boss_hp,
            "seconds_left": current_fight.seconds_left,
            "ends_at": current_fight.ends_at,
        }
    )
    data = request.data

    username = data.get("username")  # test fail case
    password = data.get("password")

    # check missing fields
    if not username or not password:
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    # check duplicate username
    if Users.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # create user with default class
    user = Users.objects.create(
        username=username,
        password=make_password(password),
        user_class="",  # Default empty class until user selects one
    )

    # Keep signup and login behavior aligned so authenticated setup pages work.
    request.session["user_id"] = user.user_id
    request.session.save()

    return Response(
        {
            "message": "User created",
            "username": user.username,
            "has_class": bool(user.user_class),  # Check if user has chosen a class
        }
    )


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Missing fields"}, status=400)

    # Get user from custom Users model
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)

    # Verify password
    if not check_password(password, user.password):
        return Response({"error": "Invalid credentials"}, status=401)

    # Store user ID in session
    request.session["user_id"] = user.user_id
    request.session.save()

    return Response(
        {
            "message": "Login successful",
            "username": user.username,
            "has_class": bool(user.user_class),  # Check if user has chosen a class
        }
    )


@api_view(["POST"])
def logout_user(request):
    request.session.flush()

    return Response({"message": "Logout successful"})


# @api_view(['POST'])
# @custom_auth_required
# def reset_habits(request):
#     updated = Habits.objects.filter(
#         user_id=request.custom_user,
#         status="Completed"
#     ).update(status="Active")

#     return Response({
#         "message": "Habits reset to Active",
#         "reset_count": updated
#     })


@api_view(["POST"])
@custom_auth_required
def choose_class(request):
    selected_class = request.data.get("user_class")
    selected_class = CLASS_ALIASES.get(selected_class, selected_class)

    if not selected_class:
        return Response({"error": "No class provided"}, status=400)

    # Get user from custom auth
    user = request.custom_user

    starting_stats = CLASS_STARTING_STATS.get(selected_class)
    if not starting_stats:
        return Response({"error": "Invalid class"}, status=400)

    user.user_class = selected_class
    user.level = 0
    user.strength = starting_stats["strength"]
    user.inteligence = starting_stats["inteligence"]
    user.charisma = starting_stats["charisma"]
    user.user_hp = starting_stats["user_hp"]
    user.save()

    return Response({"message": "Class selected", "class": user.user_class})

@api_view(["POST"])
@custom_auth_required
def start_current_fight(request):
    user = request.custom_user
    boss_id = request.data.get("boss_id") or 1

    if CurrentFight.objects.filter(user_id=user).exists():
        return Response({"error": "Already in a fight"}, status=400)

    try:
        boss = Bosses.objects.get(boss_id=boss_id)
    except Bosses.DoesNotExist:
        return Response({"error": "Boss not found"}, status=404)

    current_fight = create_current_fight(user=user, boss=boss)

    return Response(
        {
            "message": "Fight started",
            "fight_id": current_fight.fight_id,
            "boss_id": boss.boss_id,
            "boss_name": boss.boss_name,
            "seconds_left": current_fight.seconds_left,
            "ends_at": current_fight.ends_at,
        }
    )



@api_view(["GET", "POST"])
def get_task_rewards(request):
    task_description = request.query_params.get("task_description") or request.data.get(
        "task_description"
    )

    user_id = request.session.get("user_id")
    if not user_id:
        return Response({"error": "Unauthorized"}, status=401)

    try:
        user = Users.objects.get(user_id=user_id)
        current_fight = ensure_current_fight(user)
        boss_max_hp = current_fight.boss_id.boss_hp
    except (Users.DoesNotExist, Bosses.DoesNotExist):
        return Response({"error": "No current fight"}, status=400)

    if not task_description:
        return Response({"error": "task_description is required"}, status=400)

    try:
        rewards = generate_task_rewards(task_description, boss_max_hp)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=502)

    return Response({"rewards": rewards})


@api_view(["POST"])
@custom_auth_required
def create_duty(request):
    user = request.custom_user
    description = request.data.get("description")
    rewards = _get_task_rewards(user.user_id, description)
    stats = rewards.get("stats", {})
    strength = stats.get("strength", 0.0)
    intelligence = stats.get("intelligence", 0.0)
    charisma = stats.get("charisma", 0.0)
    deadline = request.data.get("deadline")

    if not description:
        return Response({"error": "Missing fields"}, status=400)

    duty = Duties.objects.create(
        user_id=user,
        description=description,
        strength=strength,
        intelligence=intelligence,
        charisma=charisma,
        deadline=deadline,
    )

    return Response(
        {
            "message": "Duty created",
            "duty_id": duty.duty_id,
            "stats": {
                "strength": strength,
                "intelligence": intelligence,
                "charisma": charisma,
            },
        }
    )


@api_view(["POST"])
@custom_auth_required
def create_habit(request):
    user = request.custom_user
    description = request.data.get("description")
    rewards = _get_task_rewards(user.user_id, description)
    stats = rewards.get("stats", {})
    strength = stats.get("strength", 0.0)
    intelligence = stats.get("intelligence", 0.0)
    charisma = stats.get("charisma", 0.0)

    if not description:
        return Response({"error": "Missing fields"}, status=400)

    try:
        rewards = _get_task_rewards(user.user_id, description)
    except ValueError as exc:
        return Response({"error": str(exc)}, status=400)

    stats = rewards.get("stats", {})
    strength = stats.get("strength", 0.0)
    intelligence = stats.get("intelligence", 0.0)
    charisma = stats.get("charisma", 0.0)

    habit = Habits.objects.create(
        user_id=user,
        description=description,
        strength=strength,
        intelligence=intelligence,
        charisma=charisma,
    )

    return Response(
        {
            "message": "Habit created",
            "habit_id": habit.habit_id,
            "stats": {
                "strength": strength,
                "intelligence": intelligence,
                "charisma": charisma,
            },
        }
    )


@api_view(["POST"])
@custom_auth_required
def update_duty_status(request, duty_id):
    user = request.custom_user
    new_status = request.data.get("status")

    if new_status not in ["Active", "Completed"]:
        return Response({"error": "Invalid status"}, status=400)
    try:
        duty = Duties.objects.get(duty_id=duty_id, user_id=user)
        if duty.status == "Completed":
            duty.status = "Active"
        else:
            duty.status = "Completed"
    except Duties.DoesNotExist:
        return Response({"error": "Duty not found"}, status=404)

    duty.save()

    return Response(
        {
            "message": "Duty status updated",
            "duty_id": duty.duty_id,
            "new_status": duty.status,
        }
    )

@api_view(["POST"])
@custom_auth_required
def update_habit_status(request, habit_id):
    user = request.custom_user
    new_status = request.data.get("status")

    if new_status not in ["Active", "Completed"]:
        return Response({"error": "Invalid status"}, status=400)
    try:
        habit = Habits.objects.get(habit_id=habit_id, user_id=user)
        if habit.status == "Completed":
            habit.status = "Active"
        else:
            habit.status = "Completed"
    except Habits.DoesNotExist:
        return Response({"error": "Habit not found"}, status=404)

    habit.save()

    return Response(
        {
            "message": "Habit status updated",
            "habit_id": habit.habit_id,
            "new_status": habit.status,
        }
    )


@api_view(["GET"])
@custom_auth_required
def get_user_info(request):
    user = request.custom_user
    user_id = request.session.get("user_id")
    duties = Duties.objects.filter(user_id=user_id).values(
        "duty_id",
        "description",
        "strength",
        "intelligence",
        "charisma",
        "status",
        "deadline",
    )
    habits = Habits.objects.filter(user_id=user_id).values(
        "habit_id", "description", "strength", "intelligence", "charisma", "status"
    )
    try:
        current_fight = serialize_current_fight(ensure_current_fight(user))
    except Bosses.DoesNotExist:
        current_fight = None

    return Response(
        {
            "user_id": user.user_id,
            "username": user.username,
            "user_class": user.user_class,
            "has_class": bool(user.user_class),
            "level": user.level,
            "strength": user.strength,
            "intelligence": user.inteligence,
            "charisma": user.charisma,
            "user_hp": user.user_hp,
            "duties": list(duties),
            "habits": list(habits),
            "current_fight": current_fight,
        }
    )


@api_view(["POST"])
@custom_auth_required
def remove_duty(request, duty_id):
    user = request.custom_user

    try:
        duty = Duties.objects.get(duty_id=duty_id, user_id=user.user_id)
    except Duties.DoesNotExist:
        return Response({"error": "Duty not found"}, status=404)

    duty.delete()

    return Response({"message": "Duty removed", "duty_id": duty_id})

@api_view(["POST"])
@custom_auth_required
def remove_habit(request, habit_id):
    user = request.custom_user

    try:
        habit = Habits.objects.get(habit_id=habit_id, user_id=user.user_id)
    except Habits.DoesNotExist:
        return Response({"error": "Duty not found"}, status=404)

    habit.delete()

    return Response({"message": "Duty removed", "habit_id": habit_id})

@api_view(["POST"])
@custom_auth_required
def setup_fight(request):
    user = request.custom_user
    boss_id = request.data.get("boss_id")

    if not boss_id:
        return Response({"error": "boss_id is required"}, status=400)

    if CurrentFight.objects.filter(user_id=user).exists():
        return Response({"error": "Already in a fight"}, status=400)

    # Get boss
    try:
        boss = Bosses.objects.get(boss_id=boss_id)
    except Bosses.DoesNotExist:
        return Response({"error": "Boss not found"}, status=404)

    current_fight = create_current_fight(user=user, boss=boss)

    return Response(
        {
            "message": "Fight started",
            "fight_id": current_fight.fight_id,
            "boss_id": boss.boss_id,
            "seconds_left": current_fight.seconds_left,
            "ends_at": current_fight.ends_at,
        }
    )

@api_view(["POST"])
@custom_auth_required
def attack_boss(request):

    user = request.custom_user

    try:
        current_fight = ensure_current_fight(user)
    except Bosses.DoesNotExist:
        return Response({"error": "No current fight"}, status=400)

    user = _populate_completed_stats(user)

    damage = (
        user.total_strength
        + user.total_intelligence
        + user.total_charisma
    )

    boss_hp = current_fight.current_boss_hp
    if boss_hp is None:
        boss_hp = current_fight.boss_id.boss_hp

    boss_hp -= damage

    if boss_hp < 0:
        boss_hp = 0

    current_fight.current_boss_hp = boss_hp
    current_fight.save()

    completed_duties.update(status="Used")
    completed_habits.update(status="Used")

    return Response({
        "attack_damage": damage,
        "damage": damage,
        "boss_hp": boss_hp,
        "boss_defeated": _is_boss_defeated(boss_hp),
    })

# Update the current fight with the new boss
@api_view(["POST"])
@custom_auth_required
def update_current_fight(request):
    user = request.custom_user
    boss_id = request.data.get("boss_id")

    if not boss_id:
        return Response({"error": "boss_id is required"}, status=400)


    # Get boss
    # Get new boss template
    try:
        boss = Bosses.objects.get(boss_id=boss_id)
    except Bosses.DoesNotExist:
        return Response({"error": "Boss not found"}, status=404)

    current_fight = CurrentFight.objects.get(user_id=user)
    current_fight = reset_current_fight(current_fight, boss)

    return Response(
        {
            "message": "Fight updated",
            "fight_id": current_fight.fight_id,
            "boss_id": boss.boss_id,
            "seconds_left": current_fight.seconds_left,
            "ends_at": current_fight.ends_at,
        }
    )

@api_view(["GET"])
def leaderboard(request):
    top_users = (
        Users.objects.order_by("-level", "-exp")
        .values("username", "level", "exp")[:5]
    )
    return Response({"leaderboard": list(top_users)})
