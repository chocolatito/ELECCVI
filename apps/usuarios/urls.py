"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import logout_view, LoginFormView  # , UserCreateView

app_name = 'usuarios'
urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path('create_user/', UserCreateView.as_view(), name='create-user'),
]
