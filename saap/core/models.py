# coding=utf-8

from django.db import models
from django import forms


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
