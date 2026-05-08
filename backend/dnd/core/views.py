from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view


@ensure_csrf_cookie
def set_csrf_token(request):
    """
    This view sets the CSRF cookie in the user's browser.
    """
    return JsonResponse({"details": "CSRF cookie set"}, status=200)

@api_view(['POST'])
def register_user(request):
    """ """