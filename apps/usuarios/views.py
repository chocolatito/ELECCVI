# from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

# from django.contrib.auth.models import User
# from django.views.generic.edit import CreateView
#
# from .forms import UserForm
# from apps.core.forms import ElectorCreateForm
# Create your views here.


class LoginFormView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar Sesión"
        return context


def logout_view(request):
    logout(request)
    return redirect('index:index')


"""
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "../templates/users/createU.html"
    success_url = reverse_lazy('core:create-elector')

    def post(self, request, *args, **kwargs):
        formU = UserForm(request.POST)
        formE = ElectorCreateForm(request.POST)
        if formU.is_valid() and formE.is_valid():
            new_user = formU.save()
            new_elector = formE.save()
            new_elector.user = new_user
            new_elector.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['formU'] = formU
        context['formE'] = formE
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formU'] = self.form_class
        context['formE'] = ElectorCreateForm
        return context
"""
