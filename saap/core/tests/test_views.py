# coding=utf-8
from core.views import *
from autenticacao.models import OrganizadorContatos
import pytest
from django.test import Client
from core.models import Ticket
from autenticacao.models import OrganizadorContatos


@pytest.mark.django_db
def test_enviar_ticket():
    client = Client()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')

    organizador.save()



    user = client.login(username='sabino', password='eusoueu0')

    request = {
    "nome_organizador":"sabino",
    "enviar_anonimamente":"False",
    "assunto" : "blablabla",
    "descricao" : "corpo_texto",
    "envio_anonimo": "anonimo",
    "tipo_mensagem": "blablabla"
    }

    response = client.post('/ticket/',request)
    tickets = Ticket.objects.all().count()

    assert tickets == 1
    Ticket.objects.all()[0].delete()


@pytest.mark.django_db
def test_deletar_ticket():
    client = Client()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')

    organizador.save()

    client.login(username='sabino', password='eusoueu0')

    request = {
    "nome_organizador":"sabino",
    "enviar_anonimamente":"False",
    "assunto" : "blablabla",
    "descricao" : "corpo_texto",
    "envio_anonimo": "anonimo",
    "tipo_mensagem": "blablabla"
    }

    client.post('/ticket/',request)

    tickets_before = Ticket.objects.all().count()

    ticket = Ticket.objects.all().last()

    client.get('/deletar_ticket/'+str(ticket.id),follow=True)

    tickets_after = Ticket.objects.all().count()
    assert tickets_before > tickets_after

@pytest.mark.django_db
def test_vereadores_view_get():

	client = Client()
	response = client.get('/vereadores/')
	assert response.status_code is 200

@pytest.mark.django_db
def test_vereadores_view_post_nao_existe():

	client = Client()
	response = client.post('/vereadores/', {'nome_organizador': ''})
	assert response.status_code is 200

@pytest.mark.django_db
def test_vereadores_view_post_existe():

	organizador = OrganizadorContatos()
	organizador.first_name = 'Organizador'
	organizador.data_de_nascimento = '1900-01-01'
	organizador.save()
	client = Client()
	response = client.post('/vereadores/', {'nome_organizador': 'Organizador'})
	assert response.status_code is 200
	organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_view_get_organizador_logado():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/gerar_carta/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_view_get_organizador_deslogado():

    cidadao = Cidadao()
    cidadao.username = 'cidteste'
    cidadao.set_password('123')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidteste', 'password': '123'})
    response = client.get('/gerar_carta/')
    assert 300 <= response.status_code < 400
    cidadao.delete()

@pytest.mark.django_db
def test_enviar_carta_view_post():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/gerar_carta/', {'nome_remetente': 'Remetente', \
        'municipio_remetente': 'Município', 'nome_destinatario': 'Destinatário'\
        , 'forma_tratamento': 'Senhor(a)', 'mensagem': 'Mensagem'})
    assert 300 <= response.status_code < 400
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_view_post_faltando_campo():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/gerar_carta/', {'nome_remetente': 'Remetente', \
        'municipio_remetente': 'Município', 'nome_destinatario': 'Destinatário'\
        , 'forma_tratamento': 'Senhor(a)', 'mensagem': ''})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_cartas_view_get_logado():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/cartas/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_cartas_view_get_deslogado():

    cidadao = Cidadao()
    cidadao.username = 'cidteste'
    cidadao.set_password('123')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidteste', 'password': '123'})
    response = client.get('/cartas/')
    assert 300 <= response.status_code < 400
    cidadao.delete()

@pytest.mark.django_db
def test_deletar_carta_view():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    carta = Carta()
    carta.save()
    organizador.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/deletar_carta/1/')
    procurar_carta = organizador.cartas.filter(id='1')
    assert procurar_carta.count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_gerar_pdf_carta_view():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    carta = Carta()
    carta.save()
    organizador.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/gerar_pdf/1/')
    assert response.status_code is 200
    carta.delete()
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_email_view():

    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    carta = Carta()
    carta.save()
    organizador.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/enviar_carta/1/', {'email_carta': 'exemplo@teste.com'})
    assert 300 <= response.status_code < 400
    carta.delete()
    organizador.delete()
