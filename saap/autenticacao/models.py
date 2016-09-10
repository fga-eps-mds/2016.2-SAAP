from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *


# Create your models here.

class Usuario_saap(User):

    data_de_nascimento = models.DateField()
    sexo = models.CharField(max_length=250)
    municipio = models.CharField(max_length=250)

    @classmethod
    def busca_nome(cls, nome):
        return Usuario_saap.objects.filter(first_name__startswith(nome))

    @classmethod
    def deleta_usuario(cls, idArg):
        Usuario_saap.objects.get(id=idArg).delete()

    @classmethod
    def busca_username(cls, username):
        return Usuario_saap.objects.filter(username__startswith(username))

    @classmethod
    def get_usuario_por_username(cls, username):
        return Usuario_saap.objects.filter(username = username)
