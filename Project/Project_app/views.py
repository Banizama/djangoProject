from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from .forms import RegUserForm
from .models import User


class HomePage(TemplateView):
    template_name = 'home_page.html'


# def register(request):
#     form = RegUserForm()
#     return render(request, 'reg_page.html', {'form': form})


class RegPage(CreateView):
    template_name = 'reg_page.html'
    success_url = reverse_lazy('login')
    form_class = RegUserForm


class LoginPage(LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('home')
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')