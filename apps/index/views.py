from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from apps.core.models import Padron, Elector, Cargo, Eleccion, Candidato
from .utils import get_index_sumary

# Create your views here.


@login_required(login_url='usuarios:login')
def index(request):
    sumary = {'usuarios': 15,
              'articulos': 0,
              'autores': 7}
    list_urls = {'usuarios': "reverse_lazy('core:usuario-list')",
                 'articulos': "reverse_lazy('core:articulo-list')",
                 'autores': "reverse_lazy('core:autor-list')"}
    print(sumary)
    for entry, value in sumary.items():
        if value:
            print(f'Total de registros de {entry}: {value}')
        else:
            print(list_urls[entry])

    return render(request, 'index.html',
                  {'title': 'Bienvenido',
                   'sumary':
                   {'Padrones': get_index_sumary(Padron.objects.all(),
                                                 'core:padron-list',
                                                 'core:create-padron'),
                    'Electores': get_index_sumary(Elector.objects.all(),
                                                  'core:elector-list',
                                                  'core:create-elector'),
                    'Cargos': get_index_sumary(Cargo.objects.all(),
                                               'core:cargo-list',
                                               'core:create-cargo'),
                    'Elecciones': get_index_sumary(Eleccion.objects.all(),
                                                   'core:eleccion-list',
                                                   'core:create-eleccion'),
                    'Candidatos': get_index_sumary(Candidato.objects.all(),
                                                   'index:index',
                                                   'core:create-candidato')
                    },
                   }
                  )
