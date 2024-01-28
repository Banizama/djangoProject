from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import home_page, registration, LoginPage, cur_user_page, logout_user, PostPage, UserPage, add_post_page, \
    search_users, edit_user_info

urlpatterns = [
    path('', login_required(home_page), name='home'),
    path('register', registration, name='register'),
    path('login', LoginPage.as_view(), name='login'),
    path('cur-user-page/logout', login_required(logout_user), name='logout'),
    path('cur-user-page', login_required(cur_user_page), name='cur_user_page'),
    path('cur-user-page/edit-user-info', login_required(edit_user_info), name='edit_user_info'),
    path('post/<int:id>/', login_required(PostPage.as_view()), name='post_page'),
    path('user/<int:id>/', login_required(UserPage.as_view()), name='user_page'),
    path('add-post', login_required(add_post_page), name='add_post'),
    path('users', login_required(search_users), name='users')

]
