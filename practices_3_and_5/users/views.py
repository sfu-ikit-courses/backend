from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterUserForm
from django.urls import reverse_lazy

# Create your views here.


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("article.index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
