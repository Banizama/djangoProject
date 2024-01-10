from .views import HomePage, RegPage, LoginPage
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegPage.as_view(), name='register'),
    path('login', LoginPage.as_view(), name='login')
]
