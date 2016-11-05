# coding=utf-8
from default.views import *
from core.models import *
from autenticacao.models import *
from autenticacao.views import *
from core.views import *
from django.test import Client
import pytest


def test_checar_campos():
    campos = ['teste']
    response = checar_campos(campos)
    assert response is True

def test_checar_campos_vazio():
    campos = ['teste','']
    response = checar_campos(campos)
    assert response == 1

def test_checar_vazio():
	campos = ['']
	assert checar_vazio(campos) is False

@pytest.mark.django_db
def test_checar_existe_usuario_existente():
    client = Client()
    response = client.post('/cadastro/', {'first_name': 'teste', \
        'last_name': 'teste', 'username': 'teste', \
        'email': 'teste@email.com', 'confirmacao_email': 'teste@email.com',\
        'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
        'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
        '1900-01-01'})
    cidadao = Cidadao.objects.filter(username='teste').count() > 0
    organizador = OrganizadorContatos.objects.filter(username='teste').count() == 0
    assert organizador is True
    assert cidadao is True

@pytest.mark.django_db
def test_checar_existe_usuario_nao_existente():
    client = Client()
    response1 = client.post('/cadastro/', {'first_name': 'teste', \
        'last_name': 'teste', 'username': 'teste', \
        'email': 'teste@email.com', 'confirmacao_email': 'teste@email.com',\
        'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
        'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
        '1900-01-01'})
    cidadao = Cidadao.objects.filter(username='teste').count() == 0
    organizador = OrganizadorContatos.objects.filter(username='teste').count() > 0
    assert organizador is False
    assert cidadao is False

@pytest.mark.django_db
def test_checar_campos_registro():
    cidadao = Cidadao()
    cidadao.username = 'cidadao'
    cidadao.set_password('123')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    campos = ['cidadao','123','1990-01-01']
    campos_validados = checar_campos(campos)
    assert campos_validados is True
    cidadao.delete()

def test_checar_data():
    teste_data = checar_data('1990-1-01')
    assert teste_data is False
