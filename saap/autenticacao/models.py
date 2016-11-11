# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *
from core.models import Contato, Ticket, Oficio, Boletim, Template, Carta


# Create your models here.

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


class Gabinete_saap(models.Model):

    participantes = models.ManyToManyField(Usuario_saap)
    nome_gabinete = models.CharField(max_length=100)
    municipio = models.CharField(max_length=250)
    uf = models.CharField(max_length=2)
    enderecoGabinete = models.CharField(max_length=300, default='')
    emailCorporativo = models.EmailField(max_length=30,default='')
    logoCasa = models.ImageField()  # Para models.ImageField funcionar deve-se fazer o seguinte em url.py:
    # urlpatterns = [ # ... the rest of your URLconf goes here ... ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""
    enderecoCasa = models.CharField(max_length=300, default='')

class Cidadao(Usuario_saap):

    pass


class OrganizadorContatos(Usuario_saap):

    contatos = models.ManyToManyField(Contato)
    tickets = models.ManyToManyField(Ticket)
    cartas = models.ManyToManyField(Carta)

class OrganizadorGabinete(Usuario_saap):

    partido = models.CharField(max_length=100,default='')
    gabinete = Gabinete_saap()
    tickets = models.ManyToManyField(Ticket)
    template = models.ManyToManyField(Template)
    documento = models.ManyToManyField(Oficio)
    boletim = models.ManyToManyField(Boletim)

class AdministradorGabinete(Usuario_saap):

    gabinetes = models.ManyToManyField(Gabinete_saap)
    cidade = models.CharField(max_length=20,default='')
    cep = models.CharField(max_length=8,default='')
    telefone_pessoal = models.CharField(max_length=7,default='',blank=True,null=True)
    telefone_gabinete = models.CharField(max_length=7,default='',blank=True,null=True)


    class Meta:
        permissions = (
                ("organizar_contatos", "Organizador de contatos"),
                ("enviar_documentos", "Organizador de Gabinete"),
                ("responder_ticket", "Administrador de Gabinete"),
                )
