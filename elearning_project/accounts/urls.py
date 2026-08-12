from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),

    # Admin
    path('admin-login/', login_view, name="login"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('logout/', logout_view, name="logout"),

    # Learner
    path('register/', register, name="register"),
    path('user-login/', user_login, name="user_login"),
    path('user-dashboard/', user_dashboard, name="user_dashboard"),
    path('user-logout/', user_logout, name="user_logout"),
    path('view-users/', view_users),
    path('delete-user/<int:user_id>/', delete_user),
]