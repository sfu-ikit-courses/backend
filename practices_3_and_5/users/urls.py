from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("login/", views.LoginUserView.as_view(), name="users.login"),
    path("logout/", LogoutView.as_view(), name="users.logout"),
    path("register/", views.RegisterUserView.as_view(), name="users.register"),
    path("profile/", views.ProfileView.as_view(), name="users.profile"),
]
