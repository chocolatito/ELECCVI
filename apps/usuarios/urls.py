"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import login_view, logout_view, UserCreateView

app_name = 'usuarios'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_user/', UserCreateView.as_view(), name='create-user'), ]
