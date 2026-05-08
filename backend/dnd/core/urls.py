from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("api/set-csrf/", views.set_csrf_token, name="set_csrf_token"),
    path("api/register/", views.register_user, name="register_user"),
    path("api/login/", views.login_user, name="login_user"),
    path("api/logout/", views.logout_user, name="logout_user"),
    path("api/reset_habits/", views.reset_habits, name="reset_habits"),
    path("api/choose_class/", views.choose_class, name="choose_class"),
    path("api/test_ai/", views.test_ai, name="test_ai"),
]

# // Next.js side
# const initializeApp = async () => {
#   await fetch('http://localhost:8000/api/set-csrf/', {
#     method: 'GET',
#     credentials: 'include', // CRITICAL: This allows the browser to save the cookie
#   });
# };
