from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from .forms import RegUserForm, PostForm, CommentForm
from .models import User, Post, Comment, Follow
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

    def Post(self):
        follow = Follow(user=1)
        follow.save()
        return redirect('/login')




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
        post = Post.objects.get(id=self.kwargs['id'])
        comment = Comment.objects.filter(post=post)
        context['comments'] = comment
        context['form'] = CommentForm()
        context['post'] = post
        return context

    def post(self, request, **kwargs):
        post = Post.objects.get(id=self.kwargs['id'])
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(text=form.cleaned_data['text'], user=request.user, post=post)
                comment.save()
            return redirect(f'/post/{post.id}')
        else:
            form = CommentForm()
        return render(request, 'post_page.html', {'form': form})


# @login_required
# class CurUserPage(TemplateView):
#     template_name = 'cur_user_page.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request


@login_required
def cur_user_page(request):
    cur_user_post = Post.objects.filter(user=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['img']
            description = form.cleaned_data['description']
            post = Post(img=img, description=description, user=request.user)
            post.save()
            return redirect('/cur_user_page')
    else:
        form = PostForm()
    return render(request, 'cur_user_page.html', {'form': form, 'posts': cur_user_post,})
                                                                # 'followers': len(follow.followers.all()), 'following': len(follow.followers.all())})


def logout_user(request):
    logout(request)
    return redirect('home')


class UserPage(TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['id'])
        context['user'] = user
        return context




