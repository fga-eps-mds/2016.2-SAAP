# coding=utf-8
from autenticacao.views import *
import pytest
from django.test import Client

@pytest.mark.django_db
def test_login_view_post_false():

	client = Client()
	username = 'teste'
	password = 'teste'
	assert client.login(username=username,password=password) is False

@pytest.mark.django_db
def test_login_view_get():

	client = Client()
	response = client.get('/login/')
	assert response.status_code is 200

def test_checar_vazio_true():

	variaveis = ['teste']
	assert checar_vazio(variaveis) 

def test_checar_vazio_false():

	variaveis = ['']
	assert checar_vazio(variaveis) is False

def test_checar_confirmacao():
	return checar_confirmacao('teste','teste')

def test_registro_view_get():

	client = Client()
	response = client.get('/cadastro/')
	assert response.status_code is 200

@pytest.mark.django_db
def test_registro_view_get_login():

	client = Client()
	client.login(username='test',password='test')
	response = client.get('/cadastro/')
	assert response.status_code is 200

