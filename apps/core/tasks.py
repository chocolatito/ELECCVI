#from django.utils import timezone

from .models import Eleccion


def set_status(id, status):
    """
    https://mattsegal.dev/simple-scheduled-tasks.html
    """
    eleccion = Eleccion.objects.get(id=id)
    print(f'Estado Antes:\n{eleccion.eleccion_estatus}\n')
    eleccion.eleccion_estatus = status
    eleccion.save()
    print(f'Estado Actual\n\t{eleccion.eleccion_estatus}\n')
