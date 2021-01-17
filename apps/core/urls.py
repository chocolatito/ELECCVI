from .views import (CandidatoListView,
                    CandidatoCreateView, CandidatoUpdateView,
                    active_candidato, deactive_candidato,
                    CargoListView, CargoCreateView, CargoUpdateView,
                    active_cargo, deactive_cargo,
                    EleccionListView, EleccionDetailView,
                    EleccionCreateView, EleccionUpdateView,
                    active_eleccion, deactive_eleccion,
                    ElectorListView,
                    ElectorCreateView, ElectorUpdateView, EleccionProgramar,
                    active_elector, deactive_elector,
                    programar_eleccion,
                    PadronListView, PadronDetailView,
                    PadronCreateView, PadronUpdateView,
                    active_padron, deactive_padron,
                    )
from django.urls import path
"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""

app_name = 'core'
urlpatterns = [
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
    # Eleccion EleccionProgramar
    path('elecciones/', EleccionListView.as_view(), name='eleccion-list'),
    path('eleccion/<int:pk>/', EleccionDetailView.as_view(), name='eleccion-detail'),
    path('create_eleccion/', EleccionCreateView.as_view(), name='create-eleccion'),
    path('edit_eleccion/<int:pk>', EleccionUpdateView.as_view(), name='edit-eleccion'),
    path('elecciones/active/<int:pk>', active_eleccion, name='active_eleccion'),
    path('elecciones/deactive/<int:pk>', deactive_eleccion, name='deactive_eleccion'),
    path('elecciones/programar/<int:pk>', EleccionProgramar.as_view(), name='programar-eleccion'),
    # Candidato
    path('candidatos/', CandidatoListView.as_view(), name='candidato-list'),
    path('create_candidato/', CandidatoCreateView.as_view(), name='create-candidato'),
    path('edit_candidato/<int:pk>', CandidatoUpdateView.as_view(), name='edit-candidato'),
    path('candidatos/active/<int:pk>', active_candidato, name='active_candidato'),
    path('candidatos/deactive/<int:pk>', deactive_candidato, name='deactive_candidato'),

]
