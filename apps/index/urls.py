"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import (index,)

app_name = 'index'
urlpatterns = [
    path('', index, name='index')]
