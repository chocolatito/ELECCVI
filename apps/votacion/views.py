from django.shortcuts import redirect
#
from django.utils.decorators import method_decorator
#
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
#
from .models import Voto
from ..eleccion.models import Eleccion, Candidato
# Create your views here.


# decorators = [login_required, group_required('administracion',)]
decorators = [login_required(login_url='usuarios:login'), ]


@method_decorator(decorators, name='dispatch')
class Votacion(DetailView):
    model = Eleccion
    template_name = "votacion/votacion.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return redirect('votacion:confirmar', slug=self.object.slug, pk=request.POST['button'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Votacion"
        return context


class Confirmar(TemplateView):
    template_name = "votacion/confirmar_voto.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = Eleccion.objects.get(slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST['button'] == "0":
            print("CANCELADO\n")
            return redirect("/")
        else:
            print("CONFIRMADO\n")
            candidato = Candidato.objects.get(pk=request.POST['button'])
            Voto.objects.create(candidato=candidato)
            return redirect("/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        return context
