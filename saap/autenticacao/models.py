from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Usuario_saap(User):

    data_de_nascimento = models.DateField()
    sexo = models.CharField(max_length=250)
    municipio = models.CharField(max_length=250)

    @classmethod
    def buscaNome(cls, nome):
        return Usuario_saap.objects.filter(first_name__startswith(nome))

    @classmethod
    def deletaUsuario(cls, idArg):
        Usuario_saap.objects.get(id=idArg).delete()
