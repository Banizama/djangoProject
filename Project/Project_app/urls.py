from django.contrib.auth.decorators import login_required

from .views import HomePage, RegPage, LoginPage, cur_user_page, logout_user, PostPage
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegPage.as_view(), name='register'),
    path('login', LoginPage.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('cur_user_page', login_required(cur_user_page), name='cur_user_page'),
    path('post/<int:id>', PostPage.as_view(), name='post_page')
]
