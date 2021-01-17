import pytz
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


# Task
def stopScheduleTask(task_id):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.remove_job(task_id)


def scheduleTask(y, m, d, h, min, obj, task_id):
    def jobSetStatus():
        print(f'Estado anterior {obj.eleccion_estatus}')
        obj.eleccion_estatus = 2
        obj.save()
        print(f'Estado actual {obj.eleccion_estatus}')

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.configure(timezone=pytz.timezone('America/Argentina/Tucuman'))
    scheduler.add_job(
        jobSetStatus,
        'date',
        run_date=datetime(y, m, d, h, min),
        id=task_id
    )
    scheduler.start()


# Task
"""def scheduleTask(y, m, d, h, min, obj):
    def jobSetStatus():
        print(f'Estado anterior {obj.eleccion_estatus}')
        obj.eleccion_estatus = 2
        obj.save()
        print(f'Estado actual {obj.eleccion_estatus}')

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.configure(timezone=pytz.timezone('America/Argentina/Tucuman'))
    scheduler.add_job(
        jobSetStatus,
        'cron',
        year=y, month=m, day=d, hour=h, minute=min,
        misfire_grace_time=None
    )
    scheduler.start()"""
