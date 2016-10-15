# coding=utf-8
from autenticacao.models import Usuario_saap
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *
# from autenticacao.models import Gabinete_saap
# from autenticacao.models import Usuario_saap
from saap import *
# from autenticacao.models import

class Contato(models.Model):

    nome = models.CharField(max_length=60,default='')
    data_de_nascimento = models.DateField('')
    sexo = models.CharField(max_length=10,default='')
    telefone = models.CharField(max_length=7,default='')
    celular = models.CharField(max_length=8,default='')
    fax = models.CharField(max_length=8,default='')
    cpf = models.CharField(max_length=15,default='')
    rg= models.CharField(max_length=13,default='')
    endereco = models.CharField(max_length=60,default='')
    cidade = models.CharField(max_length=20,default='')
    cep = models.CharField(max_length=8,default='')
    estado = models.CharField(max_length=20,default='')
    email = models.EmailField(max_length=30,default='')
    grupo = models.CharField(max_length=20,default='')
    titulo = models.CharField(max_length=30,default='')
    titulo_de_eleitor = models.CharField(max_length=30,default='')
    zona = models.CharField(max_length=30,default='')
    secao = models.CharField(max_length=30,default='')
    profissao = models.CharField(max_length=30,default='')
    cargo = models.CharField(max_length=30,default='')
    empresa = models.CharField(max_length=30,default='')
    dependente_nome = models.CharField(max_length=30,default='')
    dependente_aniversario = models.CharField(max_length=30,default='')
    dependente_parentesco = models.CharField(max_length=30,default='')
    dependente_partido = models.CharField(max_length=30,default='')
    dependente_data_filiacao = models.DateField('')

class Ticket(models.Model):

    envio_identificado = models.BooleanField(default=False)
    titulo = models.CharField(max_length=100)
    corpo_texto = models.CharField(max_length=500)
    remetente = models.CharField(max_length=250)
    # gabinete_destino = Gabinete_saap()
    data_publicacao = models.DateField('data_de_publicacao', auto_now=True)
    tipo_ticket = models.CharField(max_length=30)

class OrganizadorGabinete(Usuario_saap):

    nome = models.CharField(max_length=100,default='')
    partido = models.CharField(max_length=100,default='')
    gabinete = Gabinete_saap()
    tickets = models.ManyToManyField(Ticket)
    template = models.ManyToManyField(Template)
    documento = models.ManyToManyField(Documento)
    boletim = models.ManyToManyField(Boletim)

class Boletim(models.Model):
    titulo_boletim = models.CharField(max_length=100)
    corpo_texto_boletim = models.CharField(max_length= 5000)

class Documento(models.Model):

    tipo_documento = models.CharField(max_length=100)
    remetente = models.CharField(max_length=100)
    titulo_documento = models.CharField(max_length=100)
    corpo_texto_doc = models.CharField(max_length=1000000)

class Template(models.Model):

    titulo_template = models.CharField(max_length=100)
    altura_pagina = models.FloatField()
    largura_pagina = models.FloatField()
    margem_superior = models.FloatField()
    margem_inferior = models.FloatField()
    margem_esquerda = models.FloatField()
    margem_direita = models.FloatField()
    altura_etiqueta = models.FloatField()
    largura_etiqueta = models.FloatField()
    espacamento_etiqueta = models.FloatField()
    etiquetas_por_linha = models.FloatField()
