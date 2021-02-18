from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# __________________________________________________
from django.utils.decorators import method_decorator
# ____________________________________________
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
#
# __________________________________________________
from .models import Elector, Padron
from .utils import get_queryset_by_state, set_active
from .forms import PadronForm


decorators = [login_required(login_url='usuarios:login'), ]


# _Elector
@method_decorator(decorators, name='dispatch')
class ElectorListView(ListView):
    model = Elector
    template_name = "padron/elector_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Electores"
        context['page'] = "Electores"
        context['message_no_queryset'] = "No hay electores registrados"
        context['estado'] = self.request.GET.get('estado')
        context['object_list'] = get_queryset_by_state(self.model, context['estado'])
        context['list_url'] = 'padron:elector-list'
        # ____________________________________________
        context['detail_url'] = 'padron:active_elector'
        context['edit_url'] = 'padron:active_elector'
        # ____________________________________________
        context['active_url'] = 'padron:active_elector'
        context['deactive_url'] = 'padron:deactive_elector'
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Usuario']
        return context


@ login_required(login_url='usuarios:login')
def active_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), True)
    return redirect('padron:elector-list')


@ login_required(login_url='usuarios:login')
def deactive_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), False)
    return redirect('padron:elector-list')


# _Padron
@method_decorator(decorators, name='dispatch')
class PadronListView(ListView):
    model = Padron
    template_name = "padron/padron_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Padrones"
        context['page'] = "Padrones"
        context['message_no_queryset'] = "No hay padrones registrados"
        context['estado'] = self.request.GET.get('estado')
        context['object_list'] = get_queryset_by_state(self.model, context['estado'])
        context['add_url'] = 'padron:add-padron'
        context['list_url'] = 'padron:padron-list'
        # ____________________________________________
        context['detail_url'] = 'padron:padron-detail'
        context['edit_url'] = 'padron:edit-padron'
        # ____________________________________________
        context['active_url'] = 'padron:active_padron'
        context['deactive_url'] = 'padron:deactive_padron'
        context['thead'] = ['Titulo', 'Fecha', 'Codigo']
        context['ver_button'] = True
        return context


@ login_required(login_url='usuarios:login')
def active_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), True)
    return redirect('padron:padron-list')


@ login_required(login_url='usuarios:login')
def deactive_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), False)
    return redirect('padron:padron-list')


@method_decorator(decorators, name='dispatch')
class PadronDetailView(DetailView):
    model = Padron
    template_name = "padron/padron_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Padron"
        id_list = list(self.object.electores.all().values_list('id', flat=True))
        context['expelled'] = Elector.objects.exclude(id__in=id_list)
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s']
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "add" in request.POST:
            el_list = [Elector.objects.get(id=id)
                       for id in request.POST.getlist('elector_disabled')]
            [self.object.electores.add(elector) for elector in el_list]
        elif "remove" in request.POST:
            el_list = [Elector.objects.get(id=id)
                       for id in request.POST.getlist('elector_enabled')]
            [self.object.electores.remove(elector) for elector in el_list]
        return self.get(request, *args, **kwargs)


class PadronCreateView(CreateView):
    model = Padron
    form_class = PadronForm
    template_name = "padron/create.html"
    success_url = reverse_lazy('padron:padron-list')

    def post(self, request, *args, **kwargs):
        form = PadronForm(request.POST)
        if form.is_valid():
            form.save()
            # obj_id = form.save().id
            # reverse_lazy('padron:padron-detail',args=[str(obj_id)])
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Registrar un padron"
        return context


class PadronUpdateView(UpdateView):
    model = Padron
    form_class = PadronForm
    template_name = "padron/create.html"
    success_url = reverse_lazy('padron:padron-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Padron"
        context['form_title'] = "Editar datos del padron"
        return context
