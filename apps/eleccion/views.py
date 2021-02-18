from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
#
from django.utils.decorators import method_decorator
#
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
#
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
# from django.views.generic.base import TemplateView
##
from django_q.models import Schedule
#
from .models import Padron, Cargo, Eleccion, Candidato
from .forms import (CargoForm,
                    EleccionForm,
                    CandidatoForm,
                    EleccionProgamadaForm)
from .utils import (set_active,
                    enable_form,
                    get_queryset_for_status,
                    get_queryset_by_state,
                    set_status
                    )
# from .decorators import group_required
# Create your views here.


# decorators = [login_required, group_required('administracion',)]
decorators = [login_required(login_url='usuarios:login'), ]


# ____________________________________________
# _Eleccion
@method_decorator(decorators, name='dispatch')
class EleccionListView(ListView):
    model = Eleccion
    template_name = "eleccion/eleccion_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Elecciones"
        context['page'] = "Listado de Elecciones"
        context['estado'] = self.request.GET.get('estado')
        context['elecciones_pasadas'] = get_queryset_for_status(self.model,
                                                                context['estado'],
                                                                [3, 4])
        context['elecciones_pendientes'] = get_queryset_for_status(self.model,
                                                                   context['estado'],
                                                                   [0, ])

        context['elecciones_programadas'] = get_queryset_for_status(self.model,
                                                                    context['estado'],
                                                                    [1, 2])
        #
        context['add_url'] = 'eleccion:add-eleccion'
        context['list_url'] = 'eleccion:eleccion-list'
        context['detail_url'] = 'eleccion:eleccion-detail'
        context['edit_url'] = 'eleccion:edit-eleccion'
        context['active_url'] = 'eleccion:active_eleccion'
        context['deactive_url'] = 'eleccion:deactive_eleccion'
        context['thead'] = ['Eleccion', 'Cargo',
                            'Fecha', 'Inicio-Cierre', 'Estado']
        return context


@method_decorator(decorators, name='dispatch')
class EleccionDetailView(DetailView):
    model = Eleccion
    template_name = "eleccion/eleccion_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eleccion"
        return context


@method_decorator(decorators, name='dispatch')
class EleccionCreateView(CreateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:eleccion-list')

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
            context['add_new_message'].append(("un PADRON registrado",
                                               reverse_lazy('padron:add-padron')))
        if not enable_form(Cargo):
            context['void_select_field'] = True
            context['add_new_message'].append(("un CARGO registrado",
                                               reverse_lazy('eleccion:add-cargo')))
        return context


@method_decorator(decorators, name='dispatch')
class EleccionUpdateView(UpdateView):
    model = Eleccion
    form_class = EleccionForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:eleccion-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            return redirect('eleccion:eleccion-detail', slug=self.object.slug)
        else:
            self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos de la elección"
        return context


@ login_required(login_url='usuarios:login')
def active_eleccion(request, pk):
    set_active(Eleccion.objects.get(pk=pk), True)
    return redirect('eleccion:eleccion-list')


@ login_required(login_url='usuarios:login')
def deactive_eleccion(request, pk):
    set_active(Eleccion.objects.get(pk=pk), False)
    return redirect('eleccion:eleccion-list')


@ method_decorator(decorators, name='dispatch')
class EleccionCandidatoCreateView(CreateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:eleccion-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['eleccion'] = Eleccion.objects.get(slug=self.kwargs['slug']).pk
        return initial

    def post(self, request, *args, **kwargs):
        form = CandidatoForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('eleccion:eleccion-detail',
                                                     args=[kwargs['slug']]))
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.request.GET.get('slug')
        context['form_title'] = "Registrar un candidato"
        return context


class EleccionProgramar(UpdateView):
    model = Eleccion
    form_class = EleccionProgamadaForm
    template_name = "eleccion/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save()
            set_status(obj, 1)
            #
            Schedule.objects.create(name=f'{obj.id} st2: {obj.get_start_datetime()}',
                                         func='apps.eleccion.tasks.set_status',
                                         args=f'{obj.id},{2}',
                                         schedule_type='O',
                                         repeats=1,
                                         next_run=obj.get_start_datetime()
                                    )
            Schedule.objects.create(name=f'{obj.id} st3: {obj.get_end_datetime()}',
                                         func='apps.eleccion.tasks.set_status',
                                         args=f'{obj.id},{3}',
                                         schedule_type='O',
                                         repeats=1,
                                         next_run=obj.get_end_datetime()
                                    )
            #
            return redirect('eleccion:eleccion-detail', slug=obj.slug)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Horario de Inicio-Cierre"
        return context


# ____________________________________________
# _Cargo


@ method_decorator(decorators, name='dispatch')
class CargoListView(ListView):
    model = Cargo
    template_name = "eleccion/cargo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Cargo"
        context['page'] = "Cargos"
        context['message_no_queryset'] = 'No hay cargos registrados'
        context['estado'] = self.request.GET.get('estado')
        context['object_list'] = get_queryset_by_state(self.model, context['estado'])
        context['add_url'] = 'eleccion:add-cargo'
        context['list_url'] = 'eleccion:cargo-list'
        # -- COMPLETAR
        context['detail_url'] = 'eleccion:edit-cargo'
        # ------------
        context['edit_url'] = 'eleccion:edit-cargo'
        context['active_url'] = 'eleccion:active_cargo'
        context['deactive_url'] = 'eleccion:deactive_cargo'
        context['thead'] = ['Cargo', 'Descripción']
        return context


@ login_required(login_url='usuarios:login')
def active_cargo(request, pk):
    set_active(Cargo.objects.get(pk=pk), True)
    return redirect('eleccion:cargo-list')


@ login_required(login_url='usuarios:login')
def deactive_cargo(request, pk):
    set_active(Cargo.objects.get(pk=pk), False)
    return redirect('eleccion:cargo-list')


@ method_decorator(decorators, name='dispatch')
class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:cargo-list')

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


@ method_decorator(decorators, name='dispatch')
class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:cargo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del cargo"
        return context


# ____________________________________________
# _Candidato
@ method_decorator(decorators, name='dispatch')
class CandidatoListView(ListView):
    model = Candidato
    template_name = "eleccion/candidato_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Candidatos"
        context['page'] = "Candidatos"
        context['message_no_queryset'] = 'No hay candidatos registrados'
        context['estado'] = self.request.GET.get('estado')
        context['object_list'] = get_queryset_by_state(self.model,
                                                       context['estado'])
        context['add_url'] = 'eleccion:add-candidato'
        context['list_url'] = 'eleccion:candidato-list'
        # 'eleccion:candidato-detail'
        context['detail_url'] = 'eleccion:edit-candidato'
        context['edit_url'] = 'eleccion:edit-candidato'
        context['active_url'] = 'eleccion:active_candidato'
        context['deactive_url'] = 'eleccion:deactive_candidato'
        context['thead'] = ['Postulación', 'Cargo', 'Elector', 'Eleccion']
        return context


@ method_decorator(decorators, name='dispatch')
class CandidatoCreateView(CreateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:candidato-list')

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


@ method_decorator(decorators, name='dispatch')
class CandidatoUpdateView(UpdateView):
    model = Candidato
    form_class = CandidatoForm
    template_name = "eleccion/create.html"
    success_url = reverse_lazy('eleccion:cargo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "Editar datos del candidato"
        return context


@ login_required(login_url='usuarios:login')
def active_candidato(request, pk):
    set_active(Cargo.objects.get(pk=pk), True)
    return redirect('eleccion:candidato-list')


@ login_required(login_url='usuarios:login')
def deactive_candidato(request, pk):
    set_active(Cargo.objects.get(pk=pk), False)
    return redirect('eleccion:candidato-list')
