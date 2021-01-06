from django.db.models import Q
from django.contrib.auth.models import User
from .models import Elector


def set_active(obj, estate):
    obj.active = estate
    obj.save()
    return None


def get_queryset_ElectorForm():
    electores = Elector.objects.all().exclude(user=None).values_list('user', flat=True)
    return User.objects.exclude(Q(id__in=electores) | Q(is_staff=True))


def get_queryset_by_state(model, state):
    if state:
        if state == 'activo':
            return model.objects.exclude(active=False)
        elif state == 'inactivo':
            return model.objects.exclude(active=True)
        else:
            return model.objects.all()
    else:
        return model.objects.all()


def enable_form(model):
    return model.objects.filter(active=True).count()
