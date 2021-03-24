from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class AuthenticationLoginView(LoginView):
    template_name = "authentication/login.html"

class AuthenticationLogoutView(LoginRequiredMixin ,LogoutView):
    template_name = "authentication/logout.html"
