from django.db import models
from ..BaseModel import Base
from ..eleccion.models import Candidato
# Create your models here.


class Voto(Base):
    candidato = models.ForeignKey(Candidato,
                                  on_delete=models.CASCADE)

    class Meta:
        ordering = ['candidato', ]
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return "{}".format(self.candidato)
