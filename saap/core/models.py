# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *
# from autenticacao.models import Gabinete_saap
# from autenticacao.models import Usuario_saap
from saap import *
# from autenticacao.models import

class Grupo(models.Model):

    nome = models.CharField(max_length=30)
    contatos = models.ManyToManyField('Contato',related_name='grupo')

    def __str__(self):
        return self.nome


    @classmethod
    def filtro_nascimento(cls,mes_do_ano):
        return  cls.objects.filter(contatos__data_de_nascimento__contains=mes_do_ano)

    @classmethod
    def filtro_cidade(cls,cidade):
        return cls.objects.filter(contatos__cidade__contains=cidade)

    @classmethod
    def filtro_genero(cls,sexo):
        return cls.objects.filter(contatos__sexo=sexo)



class Contato(models.Model):

    nome = models.CharField(max_length=60,default='')
    data_de_nascimento = models.DateField('')
    sexo = models.CharField(max_length=10,default='')
    endereco = models.CharField(max_length=60,default='')
    cidade = models.CharField(max_length=20,default='')
    cep = models.CharField(max_length=8,default='')
    estado = models.CharField(max_length=20,default='')
    email = models.EmailField(max_length=30,default='')
    telefone = models.CharField(max_length=7,default='',blank=True,null=True)
    celular = models.CharField(max_length=8,default='',blank=True,null=True)
    fax = models.CharField(max_length=8,default='',blank=True,null=True)
    cpf = models.CharField(max_length=15,default='',blank=True,null=True)
    rg= models.CharField(max_length=13,default='',blank=True,null=True)
    titulo = models.CharField(max_length=30,default='',blank=True,null=True)
    titulo_de_eleitor = models.CharField(max_length=30,default='',blank=True,null=True)
    zona = models.CharField(max_length=30,default='',blank=True,null=True)
    secao = models.CharField(max_length=30,default='',blank=True,null=True)
    profissao = models.CharField(max_length=30,default='',blank=True,null=True)
    cargo = models.CharField(max_length=30,default='',blank=True,null=True)
    empresa = models.CharField(max_length=30,default='',blank=True,null=True)
    dependente_nome = models.CharField(max_length=30,default='',blank=True,null=True)
    dependente_aniversario = models.CharField(max_length=30,default='',blank=True,null=True)
    dependente_parentesco = models.CharField(max_length=30,default='',blank=True,null=True)
    dependente_partido = models.CharField(max_length=30,default='',blank=True,null=True)
    dependente_data_filiacao = models.DateField('',blank=True,null=True)

class Ticket(models.Model):

    envio_identificado = models.BooleanField(default=False)
    titulo = models.CharField(max_length=100)
    corpo_texto = models.CharField(max_length=500)
    remetente = models.CharField(max_length=250)
    # gabinete_destino = Gabinete_saap()
    data_publicacao = models.DateField('data_de_publicacao', auto_now=True)
    tipo_ticket = models.CharField(max_length=30)
    aprovado = models.BooleanField(default=False)
    #file = models.FileField()

class Boletim(models.Model):
    titulo_boletim = models.CharField(max_length=100)
    corpo_texto_boletim = models.CharField(max_length= 5000)

class Oficio(models.Model):

    tipo_documento = models.CharField(max_length=100)
    remetente = models.CharField(max_length=100)
    destinatario = models.CharField(max_length=100)
    titulo_documento = models.CharField(max_length=100)
    corpo_texto_doc = models.CharField(max_length=1000000)
    data = models.DateField('data', auto_now=True)

    @classmethod
    def busca_por_titulo(cls, titulo_doc):
        return Oficio.objects.filter(titulo_documento__startswith=titulo_doc)

class Carta(models.Model):

    nome_remetente = models.CharField(max_length=30)
    municipio_remetente = models.CharField(max_length=30)
    nome_destinatario = models.CharField(max_length=30)
    forma_tratamento = models.CharField(max_length=30)
    texto = models.CharField(max_length=1500)
    data = models.DateField('data', auto_now=True)

class Template(models.Model):

    nome_remetente = models.CharField(max_length=30)
    municipio_remetente = models.CharField(max_length=30)
    nome_destinatario = models.CharField(max_length=30)
    forma_tratamento = models.CharField(max_length=30)
    texto = models.CharField(max_length=1500)
    data = models.DateField('data', auto_now=True)

class AdminGabinete(models.Model):
    #gabinetes = models.ManyToManyField(Gabinete)
    nome_admin = models.CharField(max_length=100)
    enderecoCasa = models.CharField(max_length=300, default='')
    enderecoGabinete = models.CharField(max_length=300, default='')
    emailCorporativo = models.EmailField(max_length=30,default='')
    logoCasa = models.ImageField()  # Para models.ImageField funcionar deve-se fazer o seguinte em url.py:
    # urlpatterns = [ # ... the rest of your URLconf goes here ... ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""

    class Meta:
        permissions = (
                ("organizar_contatos", "Organizador de contatos"),
                ("enviar_documentos", ""),
                ("responder_ticket", "Administrador de Gabinete"),
                )
