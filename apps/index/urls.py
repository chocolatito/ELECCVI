"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import Index, Sumary

app_name = 'index'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('resumen/', Sumary.as_view(), name='sumary'),
]
