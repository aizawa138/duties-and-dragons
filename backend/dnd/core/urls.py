from django.urls import URLPattern, path
from . import views

from .views import register_user

urlpatterns = [
    path("api/set-csrf/", views.set_csrf_token, name="set_csrf_token"),
    path('register/', views.register_user),
    path('login/', views.login_user),
]

# // Next.js side
# const initializeApp = async () => {
#   await fetch('http://localhost:8000/api/set-csrf/', {
#     method: 'GET',
#     credentials: 'include', // CRITICAL: This allows the browser to save the cookie
#   });
# };
