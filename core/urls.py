# core/urls.py
from django.urls import path

from .views import index, hello

urlpatterns = [
    path('', index),
    path('hello/', hello),
]