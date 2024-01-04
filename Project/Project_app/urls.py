from .views import HomePage
from django.urls import path

urlpatterns = [
    path('', HomePage.as_view())
]
