from django.shortcuts import render
from functools import wraps

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login, logout
from .models import Users

#AI import
from google import genai

# Custom authentication decorator for custom Users model
def custom_auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
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

@api_view(['POST'])
def register_user(request):
    data = request.data

    username = data.get('username') #test fail case
    password = data.get('password')

    # check missing fields
    if not username or not password:
        return Response(
            {"error": "Missing fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # check duplicate username
    if Users.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # create user with default class
    user = Users.objects.create(
        username=username,
        password=make_password(password),
        user_class=""  # Default empty class until user selects one
    )

    return Response({
        "message": "User created",
        "username": user.username,
        "has_class": bool(user.user_class)  # Check if user has chosen a class
    })

@api_view(['POST'])
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
    request.session['user_id'] = user.user_id
    request.session.save()

    return Response({
        "message": "Login successful",
        "username": user.username,
        "has_class": bool(user.user_class)  # Check if user has chosen a class
    })

@api_view(['POST'])
def logout_user(request):
    # Clear custom session
    if 'user_id' in request.session:
        del request.session['user_id']
    request.session.save()

    return Response({
        "message": "Logout successful"
    })

@api_view(['POST'])
@custom_auth_required
def choose_class(request):
    selected_class = request.data.get('user_class')

    if not selected_class:
        return Response({
            "error": "No class provided"
        }, status=400)

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
        return Response({
            "error": "Invalid class"
        }, status=400)

    user.save()

    return Response({
        "message": "Class selected",
        "class": user.user_class
    })

def test_ai(request):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Explain how AI works in a few words",
        )
        return JsonResponse({
            "message": "AI test successful",
            "response": response.text
        })
    except Exception as e:
        return JsonResponse({
            "error": f"AI test failed: {str(e)}"
        }, status=500)