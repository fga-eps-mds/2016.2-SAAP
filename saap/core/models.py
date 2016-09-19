# coding=utf-8

from django.db import models
from django import forms



# Create your models here.

class Contato(models.Model):

    nome = models.CharField(max_length=60,default='')
    data_de_nascimento = models.DateField(default='0000-00-00')
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
