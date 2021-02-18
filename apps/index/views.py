# from django.shortcuts import render
# from django.urls import reverse_lazy
#
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
#
from django.contrib.auth.decorators import login_required
#
from ..eleccion.models import Eleccion
# Create your views here.

# decorators = [login_required, group_required('administracion',)]
decorators = [login_required(login_url='usuarios:login'), ]


@method_decorator(decorators, name='dispatch')
class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bienvenido'
        # method for utils.py
        context['upcoming_elecciones'] = Eleccion.objects.filter(status=1)
        context['current_elecciones'] = Eleccion.objects.filter(status=2)
        #context['current_elecciones'] = Eleccion.objects.filter(status=2)
        print(context)
        return context


# decoratorsAdm = [login_required, group_required('administracion',)]
# @method_decorator(decoratorsAdm, name='dispatch')
class Sumary(TemplateView):
    template_name = "sumary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resumen'
        return context
