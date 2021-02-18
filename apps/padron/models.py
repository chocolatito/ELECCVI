import datetime

from django.db import models
from django.urls import reverse
# # #
from django.utils.text import slugify
# # # #
from django.db.models.signals import post_save
from django.contrib.auth.models import User
#
from ..BaseModel import Base
# _________________________________________


class Elector(Base):
    dni = models.IntegerField(null=False, blank=False,
                              default=0, verbose_name="DNI")
    names = models.CharField(verbose_name="Nombre/s",
                             max_length=100, null=False, blank=False)
    surnames = models.CharField(verbose_name="Apellido/s",
                                max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['surnames', 'names']
        verbose_name = "Elector"
        verbose_name_plural = "Electores"

    def get_absolute_url(self):
        # return reverse('core:padron-detail', args=[str(self.id)])
        return reverse('index:index', args=[str(self.id)])

    def get_field_values(self):
        return [self.dni, self.names, self.surnames, self.user]

    def get_field_values_for_padron(self):
        return [self.dni, self.names, self.surnames]

    def __str__(self):
        return "{} - {}, {}".format(self.dni, self.names, self.surnames)


class Padron(Base):
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
        return reverse('padron:padron-detail', args=[str(self.id)])

    def get_field_values(self):
        return [self.title, self.date, self.slug]

    def __str__(self):
        return "{}/{} {}".format(self.date, self.id, self.title)


#
# PRE/POST SAVE
def set_slug_Padron(sender, instance, *args, **kwargs):
    if instance.id and instance.date and not instance.slug:
        instance.slug = slugify(f'{instance.date}__{instance.id}')
        instance.save()


post_save.connect(set_slug_Padron, sender=Padron)
