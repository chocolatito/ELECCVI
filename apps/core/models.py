import uuid
import datetime
from datetime import datetime as dt

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class BaseCore(models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True


ELECCION_ESTATUS = [(0, "Pendiente"), (1, "Programada"), (2, "En curso"),
                    (3, "Finalizada"), (4, "Suspendida"), (5, "Potergada")]


class Eleccion(BaseCore):
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50, null=False, blank=False, unique=True)
    eleccion_estatus = models.IntegerField(choices=ELECCION_ESTATUS, default=0)
    # Relationships
    eleccion_padron = models.ForeignKey('Padron', on_delete=models.SET_NULL, null=True)
    eleccion_cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True)

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
        if self.eleccion_estatus == 0:
            return [self.title, self.eleccion_cargo,
                    self.date.strftime("%d-%m-%Y"),
                    '00:00-00:00',
                    self.get_eleccion_estatus_display()]
        else:
            return [self.title, self.eleccion_cargo,
                    self.date.strftime("%d-%m-%Y"),
                    f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}',
                    self.get_eleccion_estatus_display()]

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
        return reverse('core:candidato-detail', args=[str(self.id)])

    def __str__(self):
        return "{} - {}".format(self.date, self.title)


class Cargo(BaseCore):
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


class Candidato(BaseCore):
    postulation_date = models.DateField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    # Relationships
    candidato_cargo = models.ForeignKey('Cargo',
                                        on_delete=models.SET_NULL, null=True)
    candidato_elector = models.ForeignKey('Elector',
                                          on_delete=models.SET_NULL, null=True)
    candidato_eleccion = models.ForeignKey('Eleccion',
                                           null=True, blank=True,
                                           on_delete=models.SET_NULL)

    class Meta:
        ordering = ['candidato_cargo', 'postulation_date']
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

    def get_absolute_url(self):
        return reverse('core:edit-candidato', args=[str(self.id)])

    def get_field_values(self):
        return [self.postulation_date,
                self.candidato_cargo,
                self.candidato_elector,
                self.candidato_eleccion]

    def __str__(self):
        return "{} - {}".format(self.candidato_elector.dni, self.candidato_cargo.name)


class Elector(BaseCore):
    dni = models.IntegerField(null=False, blank=False,
                              default=0, verbose_name="DNI")
    names = models.CharField(verbose_name="Nombre/s",
                             max_length=100, null=False, blank=False)
    surnames = models.CharField(verbose_name="Apellido/s",
                                max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['surnames', 'names']
        verbose_name = "Elector"
        verbose_name_plural = "Electores"

    def get_field_values(self):
        return [self.dni, self.names, self.surnames, self.user]

    def get_field_values_for_padron(self):
        return [self.dni, self.names, self.surnames]

    def __str__(self):
        return "{} - {}, {}".format(self.dni, self.names, self.surnames)


class Padron(BaseCore):
    title = models.CharField(max_length=100, null=False, blank=True)
    date = models.DateField(default=datetime.date.today)
    slug = models.SlugField(null=False, blank=False, unique=True)
    # Relationships
    electores = models.ManyToManyField('Elector')

    class Meta:
        ordering = ['date', 'id']
        verbose_name = "Padron"
        verbose_name_plural = "Padrones"

    def get_absolute_url(self):
        return reverse('core:padron-detail', args=[str(self.id)])

    def get_field_values(self):
        return [self.title, self.date, self.slug]

    @property
    def get_slug(self):
        return "{}_{}".format(self.date, self.id)

    def __str__(self):
        return "{}/{} {}".format(self.date, self.id, self.title)


class Sufragio(BaseCore):
    sufragio_eleccion = models.OneToOneField('Eleccion',
                                             on_delete=models.CASCADE)
    sufragio_elector = models.OneToOneField('Elector',
                                            on_delete=models.CASCADE)
    has_voted = models.BooleanField(default=False)
    hash = models.UUIDField(default=uuid.uuid4)
    voting_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('sufragio_eleccion', 'sufragio_elector')]
        ordering = ['sufragio_eleccion', 'sufragio_elector']
        verbose_name = "Sufragio"
        verbose_name_plural = "Sufragios"

    def __str__(self):
        return "{} - {} - {}".format(self.sufragio_elector, self.voting_time, self.hash)


class Voto(BaseCore):
    candidato = models.OneToOneField('Candidato',
                                     on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['candidato', ]
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return "{}".format(self.candidato)
# _____________________________________________________


def set_slug_Padron(sender, instance, *args, **kwargs):
    print(slugify(f'{instance.date}__{instance.id}_{instance.title}'))
    if instance.id and instance.title and instance.date and not instance.slug:
        instance.slug = slugify(f'{instance.date}__{instance.id}_{instance.title}')
        instance.save()


def set_slug_Eleccion(sender, instance, *args, **kwargs):
    if instance.id and instance.title and instance.date and not instance.slug:
        instance.slug = slugify(f'{instance.date}__{instance.id}_{instance.title}')
        instance.save()


post_save.connect(set_slug_Padron, sender=Padron)
post_save.connect(set_slug_Eleccion, sender=Eleccion)
