"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'eleccion'
urlpatterns = [
    # _Cargo
    path('cargos/', views.CargoListView.as_view(), name='cargo-list'),
    path('cargos/active/<int:pk>', views.active_cargo, name='active_cargo'),
    path('cargos/deactive/<int:pk>', views.deactive_cargo, name='deactive_cargo'),
    path('cargos/add/', views.CargoCreateView.as_view(), name='add-cargo'),
    path('cargos/edit/<int:pk>/', views.CargoUpdateView.as_view(), name='edit-cargo'),
    # _Candidato
    path('candidatos/', views.CandidatoListView.as_view(), name='candidato-list'),
    path('candidatos/active/<int:pk>', views.active_candidato, name='active_candidato'),
    path('candidatos/deactive/<int:pk>',
         views.deactive_candidato, name='deactive_candidato'),
    path('candidatos/add/', views.CandidatoCreateView.as_view(), name='add-candidato'),
    path('candidatos/edit/<int:pk>/',
         views.CandidatoUpdateView.as_view(), name='edit-candidato'),
    # _ Eleccion
    path('', views.EleccionListView.as_view(), name='eleccion-list'),
    path('active/<int:pk>', views.active_eleccion, name='active_eleccion'),
    path('deactive/<int:pk>', views.deactive_eleccion, name='deactive_eleccion'),
    path('add/', views.EleccionCreateView.as_view(), name='add-eleccion'),
    # path('edit/<int:pk>/', views.EleccionUpdateView.as_view(), name='edit-eleccion'),
    path('edit/<slug:slug>/', views.EleccionUpdateView.as_view(), name='edit-eleccion'),
    path('<slug:slug>/', views.EleccionDetailView.as_view(), name='eleccion-detail'),
    path('<slug:slug>/add-candidato',
         views.EleccionCandidatoCreateView.as_view(), name='eleccion-candidato'),
    path('<slug:slug>/programar/',
         views.EleccionProgramar.as_view(), name='programar-eleccion'),

]
