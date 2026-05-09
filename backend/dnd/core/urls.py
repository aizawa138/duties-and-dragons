from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path("api/set-csrf/", views.set_csrf_token, name="set_csrf_token"),
    path("api/register/", views.register_user, name="register_user"),
    path("api/login/", views.login_user, name="login_user"),
    path("api/logout/", views.logout_user, name="logout_user"),
    path("api/choose_class/", views.choose_class, name="choose_class"),
    path("api/create_duty/", views.create_duty, name="create_duty"),
    path("api/create_habit/", views.create_habit, name="create_habit"),
    path("api/update_duty_status/", views.update_duty_status, name="update_duty_status"),
    path("api/get_task_rewards/", views.get_task_rewards, name="get_task_rewards"),
    path("api/test_ai/", views.test_ai, name="test_ai"),
    path("api/get_user_info/", views.get_user_info, name="get_user_info"),
    path("api/remove_duty/", views.remove_duty, name="remove_duty"),
]

# // Next.js side
# const initializeApp = async () => {
#   await fetch('http://localhost:8000/api/set-csrf/', {
#     method: 'GET',
#     credentials: 'include', // CRITICAL: This allows the browser to save the cookie
#   });
# };
