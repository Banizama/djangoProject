from django.contrib.auth.decorators import login_required
from .views import home_page, registration, LoginPage, cur_user_page, logout_user, PostPage, UserPage, like
from django.urls import path

urlpatterns = [
    path('', home_page, name='home'),
    path('register', registration, name='register'),
    path('login', LoginPage.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('cur_user_page', login_required(cur_user_page), name='cur_user_page'),
    path('post/<int:id>/', PostPage.as_view(), name='post_page'),
    path('user/<int:id>', login_required(UserPage.as_view()), name='user_page'),
    path('post/<int:id>/like', login_required(like), name='like'),
]
