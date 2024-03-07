from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('weather', views.weather, name='weather'),
    path('city/<int:id>', views.city, name='city'),
    path('auth/jwt', views.auth, name='api_token_auth'),
]
