# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *
from core.models import *


# Create your models here.


class Gabinete(models.Model):

    contatos = models.ManyToManyField(Contato)
    tickets = models.ManyToManyField(Ticket)
    cartas = models.ManyToManyField(Carta)
    oficios = models.ManyToManyField(Oficio)
    grupos = models.ManyToManyField(Grupo)
    nome_gabinete = models.CharField(max_length=60,default='')
    telefone_gabinete = models.CharField(max_length=7,default='',blank=True,null=True)
    endereco_gabinete = models.CharField(max_length=60,default='')
    cidade_gabinete = models.CharField(max_length=20,default='')
    cep_gabinete = models.CharField(max_length=8,default='')

class Usuario_saap(User):

    data_de_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    municipio = models.CharField(max_length=250)
    uf = models.CharField(max_length=2)

    @classmethod
    def busca_nome(cls, nome):
        return Usuario_saap.objects.filter(first_name__startswith=nome)

    @classmethod
    def deleta_usuario(cls, idArg):
        Usuario_saap.objects.get(id=idArg).delete()

    @classmethod
    def busca_username(cls, username):
        return Usuario_saap.objects.filter(username__startswith=username)

    @classmethod
    def get_usuario_por_username(cls, username):
        return Usuario_saap.objects.filter(username=username)

class Cidadao(Usuario_saap):

    pass

class OrganizadorContatos(Usuario_saap):

    gabinete = models.ForeignKey(Gabinete)

class AdministradorGabinete(Usuario_saap):

    gabinete = models.ForeignKey(Gabinete)
