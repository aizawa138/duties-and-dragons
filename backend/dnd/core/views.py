from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login, logout
from .models import Users


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
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # create user
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )

    return Response({
        "message": "User created",
        "username": user.username
    })

@api_view(['POST'])
def login_user(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Missing fields"}, status=400)

    # authenticate user
    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    # log user in (session-based)
    login(request, user)

    return Response({
        "message": "Login successful",
        "username": user.username
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def choose_class(request):

    selected_class = request.data.get('user_class')

    if not selected_class:
        return Response({
            "error": "No class provided"
        }, status=400)

    # find current user in database
    user = Users.objects.get(user_id=request.user.id)

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
