from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import RegUserForm, PostForm, CommentForm, LoginForm, EditUserInfo
from .models import User, Post, Comment, Follow


# def cur_user_followers(request):
#     cur_user = request.user
#     follows = Follow.objects.filter(user=cur_user)
#     for i in follows:
#         followers = i.followers
#     return render(request,'cur_user_followers.html', context = {'followers': followers})


def home_page(request):
    search_query = request.GET.get('search', None)
    if search_query:
        posts = Post.objects.filter(description__icontains=search_query)
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main_page.html', context={'posts': posts, 'page_obj': page_obj})


def registration(request):
    if request.method == 'POST':
        form = RegUserForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            follow = Follow(user=user)
            follow.save()
            return redirect('login')
    else:
        form = RegUserForm()
    return render(request, 'reg_page.html', context={'form': form})


class LoginPage(LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('home')
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('cur_user_page')


class PostPage(TemplateView):
    template_name = 'post_page.html'

    def get_context_data(self, **kwargs):
        data = self.request.POST
        print(data)
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
        if 'like_id' in data.keys():
            print('Like')
            if request.user not in post.like.all():
                post.like.add(request.user)
                post.save()
                return JsonResponse({'like': 'Liked', 'likes': len(post.like.all())}, safe=False)
            else:
                post.like.remove(request.user)
                post.save()
                return JsonResponse({'like': 'Like', 'likes': len(post.like.all())}, safe=False)
        else:
            print('Comment')
            print(data)
            comment = Comment(text=form.data['text'], user=request.user, post=post)
            comment.save()
            resp = render_to_string('resp.html', {'comment': comment})
            return JsonResponse(resp, safe=False)


@login_required
def cur_user_page(request):
    cur_user_post = Post.objects.filter(user=request.user.id)
    follow = Follow.objects.get(user=request.user)
    return render(request, 'cur_user_page.html', {'posts': cur_user_post,
                                                  'followers': len(follow.followers.all()),
                                                  'following': len(follow.following.all()),
                                                  'len_posts': len(cur_user_post)
                                                  })


def search_users(request):
    search_query = request.GET.get('search_user', None)
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()
    return render(request, 'search_user.html', {'users': users})


def add_post_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # comments
        if form.is_valid():
            img = form.cleaned_data['img']
            description = form.cleaned_data['description']
            post = Post(img=img, description=description, user=request.user)
            post.save()
            return redirect('cur_user_page')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def edit_user_info(request):
    cur_user = request.user
    if request.method == 'POST':
        form = EditUserInfo(request.POST, request.FILES)
        if form.is_valid():
            cur_user.image = form.cleaned_data['image']
            cur_user.username = form.cleaned_data['username']
            cur_user.email = form.cleaned_data['email']
            cur_user.save()
            return redirect('cur_user_page')
    else:
        form = EditUserInfo(initial={'username': cur_user.username, 'email': cur_user.email, 'image': cur_user.image})
        return render(request, 'edit_user_info.html', context={'form': form})


class UserPage(TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['id'])
        posts = Post.objects.filter(user=user)
        follow = Follow.objects.filter(user=user)
        for i in follow:
            context['following'] = len(i.following.all())
            context['followers'] = len(i.followers.all())
            context['just_followers'] = i.followers.all()
        context['user'] = user
        context['posts'] = posts
        context['len_posts'] = len(posts)
        context['cur_user'] = self.request.user
        return context

    def post(self, request, **kwargs):
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


