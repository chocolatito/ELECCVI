from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
#
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .utils import set_active, get_queryset_by_state, enable_form
from .models import Padron, Elector, Cargo, Eleccion, Candidato
from .forms import (ElectorCreateForm, ElectorEditForm,
                    PadronForm,
                    CargoForm,
                    EleccionForm,
                    CandidatoForm)
# Create your views here.


@login_required(login_url='login')
def index(request):
    return render(request,
                  'index.html',
                  {'sumary': {'Padrones': Padron.objects.all().count(),
                              'Electores': Elector.objects.all().count(),
                              'Cargos': Cargo.objects.all().count(),
                              'Elecciones': Eleccion.objects.all().count(),
                              'Candidatos': Candidato.objects.all().count()}})


# _Eleccion
class EleccionListView(LoginRequiredMixin, ListView):
    model = Eleccion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Elecciones"
        context['message_no_queryset'] = 'No hay elecciones registradas'
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-eleccion'
        context['list_url'] = 'core:eleccion-list'
        return context


class EleccionCreateView(CreateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:eleccion-list')

    def post(self, request, *args, **kwargs):
        form = EleccionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Registrar una elección"
        context['add_new_message'] = []
        if not enable_form(Padron):
            context['void_select_field'] = True
            context['add_new_message'].append(("Necesita al menos un PADRON registrado",
                                               reverse_lazy('core:create-padron')))
        if not enable_form(Cargo):
            context['void_select_field'] = True
            context['add_new_message'].append(("Necesita menos un CARGO registrado",
                                               reverse_lazy('core:create-cargo')))
        return context


class EleccionUpdateView(UpdateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:eleccion-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos de la elección"
        return context


# _Elector
class ElectorListView(ListView):
    model = Elector

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Electores"
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'create-user'
        context['list_url'] = 'core:elector-list'
        context['detail_url'] = 'core:elector-detail'
        context['edit_url'] = 'core:edit-elector'
        context['active_url'] = 'core:active_elector'
        context['deactive_url'] = 'core:deactive_elector'
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Usuario']
        return context


@ login_required(login_url='login')
def active_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), True)
    return redirect('core:elector-list')


@ login_required(login_url='login')
def deactive_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), False)
    return redirect('core:elector-list')


class ElectorCreateView(CreateView):
    model = Elector
    form_class = ElectorCreateForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:elector-list')

    def post(self, request, *args, **kwargs):
        form = ElectorCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Registrar un elector"
        return context


class ElectorUpdateView(UpdateView):
    model = Elector
    form_class = ElectorEditForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:elector-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del elector"
        return context


# _Padron
class PadronListView(ListView):
    model = Padron

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Padrones"
        context['message_no_queryset'] = 'No hay padrones registrados'
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-padron'
        context['list_url'] = 'core:padron-list'
        context['detail_url'] = 'core:padron-detail'
        context['edit_url'] = 'core:edit-padron'
        context['active_url'] = 'core:active_padron'
        context['deactive_url'] = 'core:deactive_padron'
        context['thead'] = ['nombre', 'fecha', 'slug']
        return context


@ login_required(login_url='login')
def active_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), True)
    return redirect('core:padron-list')


@ login_required(login_url='login')
def deactive_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), False)
    return redirect('core:padron-list')


class PadronDetailView(DetailView):

    model = Padron

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Padron"
        id_list = list(self.object.electores.all().values_list('id', flat=True))
        context['expelled'] = Elector.objects.exclude(id__in=id_list)
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Usuario']
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
    template_name = "core/create.html"
    # success_url = reverse_lazy('core:padron-list')

    def post(self, request, *args, **kwargs):
        form = PadronForm(request.POST)
        if form.is_valid():
            obj_id = form.save().id
            return HttpResponseRedirect(reverse_lazy('core:padron-detail',
                                                     args=[str(obj_id)]))
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
    template_name = "core/create.html"
    success_url = reverse_lazy('core:padron-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del padron"
        return context


# _Cargo
class CargoListView(ListView):
    model = Cargo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Cargo"
        context['message_no_queryset'] = 'No hay cargos registrados'
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-cargo'
        context['list_url'] = 'core:cargo-list'
        return context


@ login_required(login_url='login')
def active_cargo(request, pk):
    set_active(Cargo.objects.get(pk=pk), True)
    return redirect('core:cargo-list')


@ login_required(login_url='login')
def deactive_cargo(request, pk):
    set_active(Cargo.objects.get(pk=pk), False)
    return redirect('core:cargo-list')


class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:cargo-list')

    def post(self, request, *args, **kwargs):
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Registrar un cargo"
        return context


class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:cargo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del cargo"
        return context


# _Candidato
class CandidatoCreateView(CreateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:cargo-list')

    def post(self, request, *args, **kwargs):
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Registrar un candidato"
        return context


class CandidatoUpdateView(UpdateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:cargo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del candidato"
        return context
