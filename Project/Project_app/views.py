from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView
from .forms import RegUserForm, PostForm, CommentForm
from .models import User, Post, Comment, Follow
from django.contrib import messages


def home_page(request):
    search_query = request.GET.get('search', None)
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()
    return render(request, 'home_page.html', context={'users': users})


# class RegPage(CreateView):
#     template_name = 'reg_page.html'
#     success_url = reverse_lazy('login')
#     form_class = RegUserForm

def registration(request):
    if request.method == 'POST':
        form = RegUserForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            follow = Follow(user=user)
            follow.save()
            return render(request, 'login_page.html')
    else:
        form = RegUserForm()
    return render(request, 'reg_page.html', context={'form': form})


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
        context['likes'] = len(post.like.all())
        context['just_likes'] = post.like.all()
        context['cur_user'] = self.request.user
        return context

    def post(self, request, **kwargs):
        data = request.POST
        print(data)
        post = Post.objects.get(id=self.kwargs['id'])
        form = CommentForm(request.POST)
        if data['like_id']:
            print('Comment')
            if form.is_valid():
                comment = Comment(text=form.cleaned_data['text'], user=request.user, post=post)
                comment.save()
            return redirect(f'/post/{post.id}')
        else:
            print('Like')

            if request.user not in post.like.all():
                post.like.add(request.user)
                post.save()
                return JsonResponse({'like': 'Liked', 'likes': len(post.like.all())}, safe=False)
            else:
                post.like.remove(request.user)
                post.save()
                return JsonResponse({'like': 'Like', 'likes': len(post.like.all())}, safe=False)


@login_required
def cur_user_page(request):
    cur_user_post = Post.objects.filter(user=request.user.id)
    follow = Follow.objects.get(user=request.user)
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
    return render(request, 'cur_user_page.html', {'form': form, 'posts': cur_user_post,
                                                  'followers': len(follow.followers.all()),
                                                  'following': len(follow.following.all()),
                                                  'len_posts': len(cur_user_post)
                                                  })


def logout_user(request):
    logout(request)
    return redirect('home')


class UserPage(TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['id'])
        follow = Follow.objects.filter(user=user)
        for i in follow:
            context['following'] = len(i.following.all())
            context['followers'] = len(i.followers.all())
            context['just_followers'] = i.followers.all()
        context['user'] = user
        context['cur_user'] = self.request.user
        return context

    def post(self, request, **kwargs):
        # data = request.POST
        user = User.objects.get(id=self.kwargs['id'])
        follow = Follow.objects.get(user=user)
        cur_follow = Follow.objects.get(user=self.request.user)
        if request.user not in follow.followers.all():
            follow.followers.add(request.user)
            follow.save()
            cur_follow.following.add(user)
            cur_follow.save()
            return JsonResponse({'follow': 'Followed', 'followers': len(follow.followers.all())}, safe=False)
        else:
            follow.followers.remove(request.user)
            follow.save()
            cur_follow.following.remove(user)
            cur_follow.save()
            return JsonResponse({'follow': 'Follow', 'followers': len(follow.followers.all())}, safe=False)






