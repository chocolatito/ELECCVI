"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'padron'
urlpatterns = [
    # Padron
    path('', views.PadronListView.as_view(), name='padron-list'),
    path('<int:pk>/', views.PadronDetailView.as_view(), name='padron-detail'),
    path('active/<int:pk>', views.active_padron, name='active_padron'),
    path('deactive/<int:pk>', views.deactive_padron, name='deactive_padron'),
    path('add/', views.PadronCreateView.as_view(), name='add-padron'),
    path('edit/<int:pk>/', views.PadronUpdateView.as_view(), name='edit-padron'),
    # Elector
    path('electores', views.ElectorListView.as_view(), name='elector-list'),
    path('electores/active/<int:pk>', views.active_elector, name='active_elector'),
    path('electores/deactive/<int:pk>', views.deactive_elector, name='deactive_elector'),
]
