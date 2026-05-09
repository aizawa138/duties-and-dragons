from django.shortcuts import render
from functools import wraps

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
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
    return JsonResponse({"details": "CSRF cookie set"}, status=200)


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
    # Clear custom session
    if "user_id" in request.session:
        del request.session["user_id"]
    request.session.save()

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

    if CurrentFight.objects.filter(user_id=user).exists():
        return Response({"error": "Already in a fight"}, status=400)

    # For simplicity, always fight the same boss for now
    boss, _ = Bosses.objects.get_or_create(
        boss_id=request.data.get("boss_id")
    )

    current_fight = CurrentFight.objects.create(user_id=user, boss_id=boss, seconds_left=300)

    return Response(
        {
            "message": "Fight started",
            "fight_id": current_fight.fight_id,
            "boss_name": boss.boss_name,
            "seconds_left": current_fight.seconds_left,
        }
    )


@api_view(["GET", "POST"])
def test_ai(request):
    task_description = request.query_params.get("task_description") or request.data.get(
        "task_description"
    )
    boss_max_hp = request.query_params.get("boss_max_hp") or request.data.get(
        "boss_max_hp"
    )

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
    user_id = request.session["user_id"]
    description = request.data.get("description")
    strength = 0.0  # request.data.get("strength", 0.0)
    intelligence = 0.0  # request.data.get("intelligence", 0.0)
    charisma = 0.0  # request.data.get("charisma", 0.0)
    deadline = request.data.get("deadline")

    if not description or not deadline:
        return Response({"error": "Missing fields"}, status=400)

    duty = Duties.objects.create(
        user_id=user_id,
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
        }
    )


@api_view(["POST"])
@custom_auth_required
def create_habit(request):
    user_id = request.session["user_id"]
    description = request.data.get("description")
    strength = 0.0  # request.data.get("strength", 0.0)
    intelligence = 0.0  # request.data.get("intelligence", 0.0)
    charisma = 0.0  # request.data.get("charisma", 0.0)

    if not description:
        return Response({"error": "Missing fields"}, status=400)

    habit = Habits.objects.create(
        user_id=user_id,
        description=description,
        strength=strength,
        intelligence=intelligence,
        charisma=charisma,
    )

    return Response(
        {
            "message": "Habit created",
            "habit_id": habit.habit_id,
        }
    )


@api_view(["POST"])
@custom_auth_required
def update_duty_status(request, duty_id):
    user = request.session["user_id"]
    new_status = request.data.get("status")

    if new_status not in ["Active", "Completed", "Used"]:
        return Response({"error": "Invalid status"}, status=400)

    try:
        duty = Duties.objects.get(duty_id=duty_id, user_id=user)
    except Duties.DoesNotExist:
        return Response({"error": "Duty not found"}, status=404)

    duty.status = new_status
    duty.save()

    return Response(
        {
            "message": "Duty status updated",
            "duty_id": duty.duty_id,
            "new_status": duty.status,
        }
    )


api_view(["GET"])
@custom_auth_required
def get_user_info(request):
    user = request.custom_user
    duties = Duties.objects.filter(username=user.username).values(
        "duty_id", "description", "strength", "intelligence", "charisma", "status"
    )
    habits = Habits.objects.filter(username=user.username).values(
        "habit_id", "description", "strength", "intelligence", "charisma", "status"
    )
    current_fight = CurrentFight.objects.filter(username=user.username).values(
        "fight_id", "boss_id", "seconds_left"
    ).first()

    return Response(
        {
            "username": user.username,
            "user_class": user.user_class,
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
def remove_duty(request):
    user = request.custom_user
    duty_id = request.data.get("duty_id")

    try:
        duty = Duties.objects.get(duty_id=duty_id, user_id=user.user_id)
    except Duties.DoesNotExist:
        return Response({"error": "Duty not found"}, status=404)

    duty.delete()

    return Response({"message": "Duty removed", "duty_id": duty_id})