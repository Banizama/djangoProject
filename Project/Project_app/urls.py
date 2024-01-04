from .views import HomePage, RegPage
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegPage.as_view(), name='register')
]
