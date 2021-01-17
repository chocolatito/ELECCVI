from .forms import (ElectorCreateForm, ElectorEditForm,
                    PadronForm,
                    CargoForm,
                    EleccionForm, EleccionProgamadaForm,
                    CandidatoForm)
from .models import Padron, Elector, Cargo, Eleccion, Candidato
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
##
from django_q.models import Schedule
from .utils import (set_active,
                    get_queryset_by_state,
                    get_queryset_for_estatus,
                    enable_form,
                    set_estatus,
                    )
# from .schedule import scheduleTask, stopScheduleTask
# Create your views here.


# _Eleccion
class EleccionListView(LoginRequiredMixin, ListView):
    model = Eleccion
    template_name = "core/list_view/eleccion_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Elecciones"
        context['entity'] = "Elecciones pasadas"
        context['message_no_queryset'] = 'No hay elecciones pasadas registradas'
        context['elecciones_pasadas'] = get_queryset_for_estatus(self.model,
                                                                 self.request.GET.get('estado'),
                                                                 [3, 4])
        context['elecciones_pendientes'] = get_queryset_for_estatus(self.model,
                                                                    self.request.GET.get('estado'),
                                                                    [0, ])

        context['elecciones_programadas'] = get_queryset_for_estatus(self.model,
                                                                     self.request.GET.get('estado'),
                                                                     [1, 2])
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-eleccion'
        context['list_url'] = 'core:eleccion-list'
        context['detail_url'] = 'core:eleccion-detail'
        context['edit_url'] = 'core:edit-eleccion'
        context['active_url'] = 'core:active_eleccion'
        context['deactive_url'] = 'core:deactive_eleccion'
        context['thead'] = ['Eleccion', 'Cargo', 'Fecha', 'Inicio-Cierre', 'Estado']
        return context


class EleccionDetailView(DetailView):
    model = Eleccion
    template_name = "core/detail_view/eleccion_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eleccion"
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


class EleccionProgramar(UpdateView):
    model = Eleccion
    form_class = EleccionProgamadaForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:eleccion-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save()
            set_estatus(obj, 1)
            #
            t1 = Schedule.objects.create(name=f'{obj.id} st2: {obj.get_start_datetime()}',
                                         func='apps.core.tasks.set_status',
                                         args=f'{obj.id},{2}',
                                         schedule_type='O',
                                         repeats=1,
                                         next_run=obj.get_start_datetime()
                                         )
            t2 = Schedule.objects.create(name=f'{obj.id} st3: {obj.get_end_datetime()}',
                                         func='apps.core.tasks.set_status',
                                         args=f'{obj.id},{3}',
                                         schedule_type='O',
                                         repeats=1,
                                         next_run=obj.get_end_datetime()
                                         )
            print(f'\nTaraea 1: {t1.next_run}\nTaraea 2: {t2.next_run}---\n')
            print(f'\nFin{obj.get_end_datetime()}\nInicio: {obj.get_start_datetime()}')
            #
            return redirect('core:eleccion-detail', pk=obj.id)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Horario de Inicio-Cierre"
        return context


@ login_required(login_url='usuarios:login')
def active_eleccion(request, pk):
    set_active(Eleccion.objects.get(pk=pk), True)
    return redirect('core:eleccion-list')


@ login_required(login_url='usuarios:login')
def deactive_eleccion(request, pk):
    set_active(Eleccion.objects.get(pk=pk), False)
    return redirect('core:eleccion-list')


@ login_required(login_url='usuarios:login')
def programar_eleccion(request, pk):
    set_estatus(Eleccion.objects.get(pk=pk), 1)
    return redirect('core:eleccion-detail', pk=pk)


@ login_required(login_url='usuarios:login')
def posponer_eleccion(request, pk):
    set_estatus(Eleccion.objects.get(pk=pk), 5)
    return redirect('core:eleccion-list')


# _Elector


class ElectorListView(ListView):
    model = Elector
    template_name = "core/list_view/elector_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Electores"
        context['entity'] = "Electores"
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'usuarios:create-user'
        context['list_url'] = 'core:elector-list'
        context['detail_url'] = 'core:elector-detail'
        context['edit_url'] = 'core:edit-elector'
        context['active_url'] = 'core:active_elector'
        context['deactive_url'] = 'core:deactive_elector'
        context['thead'] = ['DNI', 'Nombre/s', 'Apellido/s', 'Usuario']
        return context


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


@ login_required(login_url='usuarios:login')
def active_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), True)
    return redirect('core:elector-list')


@ login_required(login_url='usuarios:login')
def deactive_elector(request, pk):
    set_active(Elector.objects.get(pk=pk), False)
    return redirect('core:elector-list')


# _Padron
class PadronListView(ListView):
    model = Padron
    template_name = "core/list_view/padron_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Padrones"
        context['entity'] = "Padrones"
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


class PadronDetailView(DetailView):
    model = Padron

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


@ login_required(login_url='usuarios:login')
def active_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), True)
    return redirect('core:padron-list')


@ login_required(login_url='usuarios:login')
def deactive_padron(request, pk):
    set_active(Padron.objects.get(pk=pk), False)
    return redirect('core:padron-list')


# _Cargo
class CargoListView(ListView):
    model = Cargo
    template_name = "core/list_view/cargo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Cargo"
        context['entity'] = "Cargos"
        context['message_no_queryset'] = 'No hay cargos registrados'
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-cargo'
        context['list_url'] = 'core:cargo-list'
        # -- COMPLETAR
        context['detail_url'] = 'core:edit-cargo'
        context['edit_url'] = 'core:edit-cargo'
        context['active_url'] = 'core:active_cargo'
        context['deactive_url'] = 'core:deactive_cargo'
        context['thead'] = ['Cargo', 'Descripción']
        return context


@ login_required(login_url='usuarios:login')
def active_cargo(request, pk):
    set_active(Cargo.objects.get(pk=pk), True)
    return redirect('core:cargo-list')


@ login_required(login_url='usuarios:login')
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
class CandidatoListView(LoginRequiredMixin, ListView):
    model = Candidato
    template_name = "core/list_view/candidato_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Candidatos"
        context['entity'] = "Candidatos"
        context['message_no_queryset'] = 'No hay candidatos registrados'
        context['object_list'] = get_queryset_by_state(self.model,
                                                       self.request.GET.get('estado'))
        context['estado'] = self.request.GET.get('estado')
        context['create_url'] = 'core:create-candidato'
        context['list_url'] = 'core:candidato-list'
        context['detail_url'] = 'core:edit-candidato'  # 'core:candidato-detail'
        context['edit_url'] = 'core:edit-candidato'
        context['active_url'] = 'core:active_candidato'
        context['deactive_url'] = 'core:deactive_candidato'
        context['thead'] = ['Postulación', 'Cargo', 'Elector', 'Eleccion']
        return context


class CandidatoCreateView(CreateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "core/create.html"
    success_url = reverse_lazy('core:candidato-list')

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
        context['id'] = self.request.GET.get('id')
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


@ login_required(login_url='usuarios:login')
def active_candidato(request, pk):
    set_active(Cargo.objects.get(pk=pk), True)
    return redirect('core:candidato-list')


@ login_required(login_url='usuarios:login')
def deactive_candidato(request, pk):
    set_active(Cargo.objects.get(pk=pk), False)
    return redirect('core:candidato-list')
