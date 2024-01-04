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
    success_url = reverse_lazy('home')
    form_class = RegUserForm
