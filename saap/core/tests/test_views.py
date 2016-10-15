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
