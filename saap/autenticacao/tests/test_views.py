# coding=utf-8
from autenticacao.views import *
from autenticacao.models import *
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

@pytest.mark.django_db
def test_login_view_post_false():

	client = Client()
	username = 'teste'
	password = 'teste'
	assert client.login(username=username,password=password) is False

@pytest.fixture
def logar_usuario(client):
	user = User(username="asdf",password="1234")
	user.set_password('123456')
	user.save()
	client.login(username=user.username, password="123456")
	return user,client

@pytest.mark.django_db
def teste_usuario_logado(client):
	user,client = logar_usuario(client)

	assert user is not None

@pytest.mark.django_db
def test_login_view_get(client):
	response = client.get('/login/')
	assert 300 >= response.status_code < 400

def test_registro_view_get():
	client = Client()
	response = client.get('/cadastro/')
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

@pytest.mark.django_db
def test_tipo_usuario_cidadao():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	response = client.post('/', {'username': 'cidadao', 'password': '123'})
	assert response.status_code is 200
	cidadao.delete()

@pytest.mark.django_db
def test_tipo_usuario_organizador_contatos():

	gabinete = Gabinete()
	gabinete.save()
	organizador = OrganizadorContatos()
	organizador.username = 'organizador'
	organizador.set_password('123')
	organizador.data_de_nascimento = '1900-01-01'
	organizador.gabinete = gabinete
	organizador.save()
	client = Client()
	response = client.post('/', {'username': 'organizador', 'password': '123'})
	assert 300 <= response.status_code and response.status_code < 400
	organizador.delete()

@pytest.mark.django_db
def test_checar_autenticacao():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	request = Client()
	request.user = authenticate(username='cidadao', password='123')
	autenticacao = checar_autenticacao(request, render(request, 'perfil.html'), 'login.html')
	assert autenticacao.status_code is 200
	cidadao.delete()

@pytest.mark.django_db
def test_mudar_senha_view_get():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.get('/mudar_senha/')
	assert response.status_code is 200
	cidadao.delete()

def test_checar_confirmacao_true():
	 response = checar_confirmacao('teste','teste')

	 assert response is True

@pytest.mark.django_db
def test_usuario_senha_errada():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	response = client.post('/', {'username': 'cidadao', 'password': '321'})
	assert response.status_code is 200
	cidadao.delete()

@pytest.mark.django_db
def test_criar_organizador_get():

	gabinete = Gabinete()
	gabinete.save()
	admin = AdministradorGabinete()
	admin.username = 'administrador'
	admin.set_password('123')
	admin.data_de_nascimento = '1900-01-01'
	admin.gabinete = gabinete
	admin.save()
	client = Client()
	client.post('/', {'username': 'administrador', 'password': '123'})
	response = client.get('/gabinete/criar_organizador/')
	assert response.status_code is 200

@pytest.mark.django_db
def test_registro_view_post_cidadao():

	client = Client()
	response = client.post('/cadastro/', {'first_name': 'Cidadão', \
		'last_name': 'Teste', 'username': 'cidadao', \
		'email': 'cidadao@teste.com', 'confirmacao_email': 'cidadao@teste.com',\
		'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
		'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
		'1900-01-01'})
	cidadao = Cidadao.objects.get(username='cidadao')
	assert cidadao is not None
	cidadao.delete()

@pytest.mark.django_db
def test_registro_view_post_cidadao_data_invalida():

	client = Client()
	response = client.post('/cadastro/', {'first_name': 'Cidadão', \
		'last_name': 'Teste', 'username': 'cidadao', \
		'email': 'cidadao@teste.com', 'confirmacao_email': 'cidadao@teste.com',\
		'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
		'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
		'1900-01-011'})
	cidadao_count = Cidadao.objects.filter(username='cidadao').count()
	assert cidadao_count == 0

@pytest.mark.django_db
def test_registro_view_post_organizador_contatos():

	gabinete = Gabinete()
	gabinete.save()
	admin = AdministradorGabinete()
	admin.username = 'administrador'
	admin.set_password('123')
	admin.data_de_nascimento = '1900-01-01'
	admin.gabinete = gabinete
	admin.save()
	client = Client()
	client.post('/', {'username': 'administrador', 'password': '123'})
	response = client.post('/gabinete/criar_organizador/', {'first_name': 'Organizador',\
		'last_name': 'Teste', 'username': 'organizador', \
		'email': 'organizador@teste.com', 'confirmacao_email': \
		'organizador@teste.com', 'password': '123', 'confirmacao_password': \
		'123', 'sexo': 'Masculino', 'municipio': 'Brasilia', 'uf': 'DF', \
		'data_de_nascimento': '1900-01-01'})
	organizador = OrganizadorContatos.objects.get(username='organizador')
	assert organizador is not None
	organizador.delete()

@pytest.mark.django_db
def test_mudar_senha_view_post():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.post('/mudar_senha/', {'nova_senha': '321', \
		'confirmacao_nova_senha': '321'})
	cidadao_teste_nova_senha = authenticate(username=cidadao.username, \
		password='321')
	assert cidadao_teste_nova_senha.username == cidadao.username
	cidadao.delete()

@pytest.mark.django_db
def test_mudar_senha_view_post_senhas_diferentes():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.post('/mudar_senha/', {'nova_senha': '111', \
		'confirmacao_nova_senha': '222'})
	cidadao_teste_senha_antiga = authenticate(username=cidadao.username, \
		password='123')
	assert cidadao_teste_senha_antiga is not None
	cidadao.delete()

@pytest.mark.django_db
def test_excluir_conta_view_get():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.get('/excluir_conta/')
	assert response.status_code is 200
	cidadao.delete()

@pytest.mark.django_db
def test_excluir_conta_view_post():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.post('/excluir_conta/', {'password': '123'})
	cidadao_teste_exclusao = authenticate(username='cidadao', password='123')
	assert cidadao_teste_exclusao is None

@pytest.mark.django_db
def test_excluir_conta_senha_errada_view_post():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.post('/excluir_conta/', {'password': '321'})
	cidadao_teste_exclusao = authenticate(username='cidadao', password='123')
	assert cidadao_teste_exclusao is not None
	cidadao.delete()

@pytest.mark.django_db
def test_registro_view_post_cidadao_ja_existe():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	response = client.post('/cadastro/', {'first_name': 'Cidadão', \
		'last_name': 'Teste', 'username': 'cidadao', \
		'email': 'cidadao@teste.com', 'confirmacao_email': 'cidadao@teste.com',\
		'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
		'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
		'1900-01-01'})
	cidadao_teste = Cidadao.objects.filter(first_name='Cidadão')
	assert cidadao_teste.count() == 0
	cidadao.delete()

@pytest.mark.django_db
def test_registro_view_post_cidadao_campo_vazio():

	client = Client()
	response = client.post('/cadastro/', {'first_name': '', \
		'last_name': 'Teste', 'username': 'cidadao', \
		'email': 'cidadao@teste.com', 'confirmacao_email': 'cidadao@teste.com',\
		'password': '123', 'confirmacao_password': '123', 'sexo': 'Masculino', \
		'municipio': 'Brasilia', 'uf': 'DF', 'data_de_nascimento': \
		'1900-01-01'})
	cidadao_teste = Cidadao.objects.filter(first_name='Cidadão')
	assert cidadao_teste.count() == 0

@pytest.mark.django_db
def test_logout_view_get():

	cidadao = Cidadao()
	cidadao.username = 'cidadao'
	cidadao.set_password('123')
	cidadao.data_de_nascimento = '1900-01-01'
	cidadao.save()
	client = Client()
	request = client.post('/', {'username': 'cidadao', 'password': '123'})
	response = client.get('/logout/')
	assert response.status_code is 200
	cidadao.delete()

@pytest.mark.django_db
def test_criar_administrador_get():

	client = Client()
	response = client.get('/criar_administrador/')
	assert response.status_code is 200

@pytest.mark.django_db
def test_registro_view_post_administrador_gabinete():

	gabinete = Gabinete()
	gabinete.nome_gabinete = 'Gabinete'
	gabinete.save()
	adms = AdministradorSistema()
	adms.username = 'adms'
	adms.set_password('123')
	adms.data_de_nascimento = '1900-01-01'
	adms.save()
	client = Client()
	client.post('/', {'username': 'adms', 'password': '123'})
	response = client.post('/administracao/criar_administrador_gabinete/', {'first_name': 'Administrador',\
		'last_name': 'Teste', 'username': 'adminGabinete', \
		'email': 'administrador@teste.com', 'confirmacao_email': \
		'administrador@teste.com', 'password': '123', 'confirmacao_password': \
		'123', 'sexo': 'Masculino', 'municipio': 'Brasilia', 'uf': 'DF', \
		'data_de_nascimento': '1900-01-01', 'cidade':'Brasilia', \
		'endereco':'endereco', 'cep': '111111111','telefone_pessoal':'61988888888',\
		'telefone_gabinete':'619222222', 'nome_gabinete': 'Gabinete'})
	admin = AdministradorGabinete.objects.get(username='adminGabinete')
	assert admin is not None
	admin.delete()
