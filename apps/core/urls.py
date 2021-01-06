"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import (index,
                    ElectorListView,
                    ElectorCreateView, ElectorUpdateView,
                    active_elector, deactive_elector,
                    PadronListView, PadronDetailView,
                    active_padron, deactive_padron,
                    CargoListView, CargoCreateView, CargoUpdateView,
                    active_cargo, deactive_cargo,
                    EleccionListView,
                    EleccionCreateView, EleccionUpdateView,
                    CandidatoCreateView, CandidatoUpdateView,
                    PadronCreateView, PadronUpdateView)

app_name = 'core'
urlpatterns = [
    path('', index, name='index'),
    # Elector
    path('create_elector/', ElectorCreateView.as_view(), name='create-elector'),
    path('elector/<int:pk>/', ElectorUpdateView.as_view(), name='elector-detail'),
    path('edit_elector/<int:pk>', ElectorUpdateView.as_view(), name='edit-elector'),
    path('electores/', ElectorListView.as_view(), name='elector-list'),
    path('electores/active/<int:pk>', active_elector, name='active_elector'),
    path('electores/deactive/<int:pk>', deactive_elector, name='deactive_elector'),
    # Padron
    path('padrones/', PadronListView.as_view(), name='padron-list'),
    path('padrones/active/<int:pk>', active_padron, name='active_padron'),
    path('padrones/deactive/<int:pk>', deactive_padron, name='deactive_padron'),
    path('padron/<int:pk>/', PadronDetailView.as_view(), name='padron-detail'),
    path('create_padron/', PadronCreateView.as_view(), name='create-padron'),
    path('edit_padron/<int:pk>', PadronUpdateView.as_view(), name='edit-padron'),
    # Cargo
    path('create_cargo/', CargoCreateView.as_view(), name='create-cargo'),
    path('edit_cargo/<int:pk>', CargoUpdateView.as_view(), name='edit-cargo'),
    path('cargos/', CargoListView.as_view(), name='cargo-list'),
    path('cargos/active/<int:pk>', active_cargo, name='active_cargo'),
    path('cargos/deactive/<int:pk>', deactive_cargo, name='deactive_cargo'),
    # Eleccion
    path('elecciones/', EleccionListView.as_view(), name='eleccion-list'),
    path('create_eleccion/', EleccionCreateView.as_view(), name='create-eleccion'),
    path('edit_eleccion/<int:pk>', EleccionUpdateView.as_view(), name='edit-eleccion'),
    # Candidato
    path('create_candidato/', CandidatoCreateView.as_view(), name='create-candidato'),
    path('edit_candidato/<int:pk>', CandidatoUpdateView.as_view(), name='edit-candidato'),

]
