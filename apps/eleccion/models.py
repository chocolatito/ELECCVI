import datetime

from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.db import models
from datetime import datetime as dt

from ..BaseModel import Base
from ..padron.models import Elector, Padron


#
# Create your models here.


ELECCION_STATUS = [(0, "Pendiente"), (1, "Programada"), (2, "En curso"),
                   (3, "Finalizada"), (4, "Suspendida"), (5, "Potergada")]


class Eleccion(Base):
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    # eleccion_estatus = models.IntegerField(choices=ELECCION_ESTATUS, default=0)
    status = models.IntegerField(choices=ELECCION_STATUS, default=0)
    # Relationships
    padron = models.ForeignKey(Padron, on_delete=models.SET_NULL, null=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True)

    @property
    def in_process(self):
        return self.start_time <= timezone.now() and timezone.now() < self.end_time

    @property
    def not_started(self):
        return timezone.now() < self.start_time

    class Meta:
        ordering = ['date', 'title']
        verbose_name = 'Eleccion'
        verbose_name_plural = 'Elecciones'

    def get_field_values(self):
        if self.status == 0:
            return [self.title, self.cargo,
                    self.date.strftime("%d-%m-%Y"),
                    '00:00-00:00',
                    self.get_status_display()]
        else:
            return [self.title, self.cargo,
                    self.date.strftime("%d-%m-%Y"),
                    f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}',
                    self.get_status_display()]

    def get_start_datetime(self):
        return dt.strptime(f'{self.date.strftime("%Y %m %d")} {self.start_time.strftime("%H %M")}',
                           "%Y %m %d %H %M")

    def get_end_datetime(self):
        return dt.strptime(f'{self.date.strftime("%Y %m %d")} {self.end_time.strftime("%H %M")}',
                           "%Y %m %d %H %M")

    def get_date_time(self):
        return [int(x)
                for x in
                f'{self.date.strftime("%Y %m %d")} {self.start_time.strftime("%H %M")}'.split(" ")]

    def get_absolute_url(self):
        return reverse('eleccion:padron-detail', args=[str(self.id)])

    def __str__(self):
        return "{} - {}".format(self.date, self.title)


class Cargo(Base):
    name = models.CharField(max_length=100,
                            null=False, blank=False,
                            verbose_name='Nombre del Cargo',
                            unique=True)
    description = models.TextField(null=False, blank=False,
                                   verbose_name='Descripción')

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def get_field_values(self):
        return [self.name, self.description]

    def __str__(self):
        return "{}".format(self.name)


class Candidato(Base):
    postulation_date = models.DateField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    # Relationships
    cargo = models.ForeignKey('Cargo',
                              on_delete=models.CASCADE, null=True)
    elector = models.ForeignKey(Elector,
                                on_delete=models.CASCADE, null=True)
    eleccion = models.ForeignKey('Eleccion',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ['cargo', 'postulation_date']
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

    def get_absolute_url(self):
        return reverse('padron:edit-padron', args=[str(self.id)])

    def get_field_values(self):
        return [self.postulation_date,
                self.cargo,
                self.elector,
                self.eleccion]

    def __str__(self):
        return "{} - {}".format(self.elector.dni, self.cargo.name)


# _______________________________________________________
# PRE/POST SAVE
def set_slug_Eleccion(sender, instance, *args, **kwargs):
    if instance.id and instance.title and instance.date and not instance.slug:
        instance.slug = slugify(f'{instance.date}__{instance.id}_{instance.title}')
        instance.save()


post_save.connect(set_slug_Eleccion, sender=Eleccion)
