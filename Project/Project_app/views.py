from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from .forms import RegUserForm, PostForm
from .models import User, Post
from django.contrib import messages


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
        return reverse_lazy('cur_user_page')


class PostPage(TemplateView):
    template_name = 'post_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(user=self.kwargs['id'])
        print(posts)
        context['posts'] = posts
        print(context)


# @login_required
# class CurUserPage(TemplateView):
#     template_name = 'cur_user_page.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request


@login_required
def cur_user_page(request):
    print(request.user.id)
    cur_user_post = Post.objects.filter(user=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['img']
            description = form.cleaned_data['description']
            post = Post(img=img, description=description, user=request.user)
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'cur_user_page.html', {'form': form, 'posts': cur_user_post})


def logout_user(request):
    logout(request)
    return redirect('home')




