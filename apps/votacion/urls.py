"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'votacion'
urlpatterns = [
    path('<slug:slug>/', views.Votacion.as_view(), name='votacion'),
    path('<slug:slug>/confirmar/<int:pk>/', views.Confirmar.as_view(), name='confirmar'),
]
