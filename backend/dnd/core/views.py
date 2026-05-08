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


# Custom authentication decorator for custom Users model
def custom_auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = Users.objects.filter(username=request.session.get("username")).first()
        if not user_id:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            request.custom_user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "Unauthorized"}, status=401)
        return func(request, *args, **kwargs)

    return wrapper


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

    if not selected_class:
        return Response({"error": "No class provided"}, status=400)

    # Get user from custom auth
    user = request.custom_user

    # update class
    user.user_class = selected_class

    # starter stats depending on class
    if selected_class == "Berserker":
        user.level = 0
        user.strength = 2
        user.inteligence = 1
        user.charisma = 1
        user.user_hp = 100
    elif selected_class == "Mage":
        user.level = 0
        user.strength = 1
        user.inteligence = 2
        user.charisma = 1
        user.user_hp = 100

    elif selected_class == "Vampire":
        user.level = 0
        user.strength = 1
        user.inteligence = 1
        user.charisma = 2
        user.user_hp = 100

    else:
        return Response({"error": "Invalid class"}, status=400)

    user.save()

    return Response({"message": "Class selected", "class": user.user_class})


@api_view(["GET"])
def test_ai(request):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Explain how AI works in a few words",
        )
        return JsonResponse(
            {"message": "AI test successful", "response": response.text}
        )
    except Exception as e:
        return JsonResponse({"error": f"AI test failed: {str(e)}"}, status=500)


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


# # Ai Functionality
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
# )

# DIFFICULTY_CAPS = {
#     "trivial": 3,
#     "easy": 5,
#     "medium": 10,
#     "hard": 20,
#     "legendary": 35,
# }


# def clamp(value, minimum, maximum):
#     return max(minimum, min(value, maximum))


# def normalize_stats(stats, max_total):
#     """
#     Ensures total stat gain does not exceed max_total.
#     """

#     total = sum(stats.values())

#     if total <= max_total:
#         return stats

#     scale = max_total / total

#     normalized = {key: max(0, round(value * scale)) for key, value in stats.items()}

#     return normalized


# def generate_task_rewards(task_title, boss_max_hp):
#     """
#     Generates balanced RPG stats for a task using OpenRouter AI.
#     """

#     prompt = f"""
#     You are balancing rewards for an RPG productivity app.

#     Analyze this task:
#     "{task_title}"

#     Return ONLY valid JSON.

#     Format:
#     {{
#         "difficulty": "trivial/easy/medium/hard/legendary",
#         "strength": number,
#         "intelligence": number,
#         "charisma": number
#     }}

#     Rules:
#     - Small daily tasks should have low rewards
#     - Harder tasks should reward more
#     - Strength = physical effort
#     - Intelligence = mental effort
#     - Charisma = social/confidence effort
#     - Keep values realistic
#     """

#     completion = client.chat.completions.create(
#         model="openai/gpt-4.1-mini",
#         messages=[
#             {"role": "system", "content": "You are a strict JSON generator."},
#             {"role": "user", "content": prompt},
#         ],
#         temperature=0.3,
#     )

#     raw = completion.choices[0].message.content

#     try:
#         data = json.loads(raw)
#     except json.JSONDecodeError:
#         raise ValueError("AI returned invalid JSON")

#     difficulty = data.get("difficulty", "easy").lower()

#     max_total = DIFFICULTY_CAPS.get(difficulty, 5)

#     stats = {
#         "strength": clamp(int(data.get("strength", 0)), 0, max_total),
#         "intelligence": clamp(int(data.get("intelligence", 0)), 0, max_total),
#         "charisma": clamp(int(data.get("charisma", 0)), 0, max_total),
#     }

#     # Normalize total stats
#     stats = normalize_stats(stats, max_total)

#     total_stats = sum(stats.values())

#     # Prevent tasks from deleting bosses instantly
#     boss_damage_cap = max(5, int(boss_max_hp * 0.05))

#     damage = clamp(total_stats, 1, boss_damage_cap)

#     return {
#         "difficulty": difficulty,
#         "stats": stats,
#         "total_stats": total_stats,
#         "boss_damage": damage,
#     }
