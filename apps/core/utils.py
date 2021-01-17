import pytz
from apscheduler.schedulers.background import BackgroundScheduler
#
from django.db.models import Q
from django.contrib.auth.models import User
#
from .models import Elector


def set_active(obj, estate):
    obj.active = estate
    obj.save()
    return None


def set_estatus(obj, state):
    obj.eleccion_estatus = state
    obj.save()


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


def get_queryset_for_estatus(model, state, estatus):
    return get_queryset_by_state(model, state).filter(eleccion_estatus__in=estatus)


def enable_form(model):
    return model.objects.filter(active=True).count()


# Task
def scheduleTask(y, m, d, h, min, obj):
    def jobSetStatus():
        print(f'Estado anterior {obj.eleccion_estatus}')
        obj.eleccion_estatus = 2
        obj.save()
        print(f'Estado actual {obj.eleccion_estatus}')

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=pytz.timezone('America/Argentina/Tucuman'))
    scheduler.add_job(
        jobSetStatus,
        'cron',
        year=y, month=m, day=d, hour=h, minute=min,
        misfire_grace_time=None
    )
    scheduler.start()
