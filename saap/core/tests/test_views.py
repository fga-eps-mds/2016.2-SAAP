# coding=utf-8
from core.views import *
from autenticacao.views import *
from autenticacao.models import OrganizadorContatos
import pytest
from django.test import Client
from core.models import Ticket
from autenticacao.models import OrganizadorContatos


@pytest.mark.django_db
def test_enviar_ticket():
    client = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')
    organizador.gabinete = gabinete

    organizador.save()

    user = client.login(username='sabino', password='eusoueu0')

    request = {
    "nome_gabinete":"Gabinete",
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
def test_enviar_ticket_campo_em_branco():
    client = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')
    organizador.gabinete = gabinete

    organizador.save()

    user = client.login(username='sabino', password='eusoueu0')

    request = {
    "nome_gabinete":"Gabinete",
    "enviar_anonimamente":"False",
    "assunto" : "blablabla",
    "descricao" : "",
    "envio_anonimo": "anonimo",
    "tipo_mensagem": "blablabla"
    }

    response = client.post('/ticket/',request)
    tickets = Ticket.objects.all().count()

    assert tickets == 0

@pytest.mark.django_db
def test_enviar_ticket_sem_autenticacao():
    client = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')
    organizador.gabinete = gabinete

    organizador.save()

    request = {
    "nome_gabinete":"Gabinete",
    "enviar_anonimamente":"False",
    "assunto" : "blablabla",
    "descricao" : "corpo_texto",
    "envio_anonimo": "anonimo",
    "tipo_mensagem": "blablabla"
    }

    response = client.post('/ticket/',request)
    tickets = Ticket.objects.all().count()

    assert tickets == 0

@pytest.mark.django_db
def test_deletar_ticket():
    client = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')
    organizador.gabinete = gabinete

    organizador.save()

    client.login(username='sabino', password='eusoueu0')

    request = {
    "nome_gabinete":"Gabinete",
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
	response = client.get('/gabinetes/')
	assert response.status_code is 200

@pytest.mark.django_db
def test_vereadores_view_post_nao_existe():

	client = Client()
	response = client.post('/gabinetes/', {'nome_gabinete': ''})
	assert response.status_code is 200

@pytest.mark.django_db
def test_vereadores_view_post_existe():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.first_name = 'Organizador'
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    response = client.post('/gabinetes/', {'nome_gabinete': 'Gabinete'})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_view_get_organizador_logado():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/gabinete/cartas/gerar_carta/')
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
    assert response.status_code > 400
    cidadao.delete()

@pytest.mark.django_db
def test_enviar_carta_view_post():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/gabinete/cartas/gerar_carta/', {'nome_remetente': 'Remetente', \
        'municipio_remetente': 'Município', 'nome_destinatario': 'Destinatário'\
        , 'forma_tratamento': 'Senhor(a)', 'mensagem': 'Mensagem'})
    assert 300 <= response.status_code < 400
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_view_post_faltando_campo():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/gabinete/cartas/gerar_carta/', {'nome_remetente': 'Remetente', \
        'municipio_remetente': 'Município', 'nome_destinatario': 'Destinatário'\
        , 'forma_tratamento': 'Senhor(a)', 'mensagem': ''})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_cartas_view_get_logado():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/gabinete/cartas/')
    assert 300 <= response.status_code < 400
    organizador.delete()

@pytest.mark.django_db
def test_enviar_oficio_view_get_organizador_logado():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    administrador = AdministradorGabinete()
    administrador.username = 'administrador'
    administrador.set_password('123456')
    administrador.data_de_nascimento = '1900-01-01'
    administrador.gabinete = gabinete
    administrador.save()
    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123456'})
    response = client.get('/gabinete/oficios/gerar_oficio/')
    assert response.status_code is 200
    administrador.delete()

@pytest.mark.django_db
def test_cartas_view_get_deslogado():

    cidadao = Cidadao()
    cidadao.username = 'cidteste'
    cidadao.set_password('123')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidteste', 'password': '123'})
    response = client.get('/gabinete/cartas/')
    assert 300 <= response.status_code < 400
    cidadao.delete()

@pytest.mark.django_db
def test_enviar_oficio_view_get_organizador_deslogado():

    cidadao = Cidadao()
    cidadao.username = 'cidteste'
    cidadao.set_password('123456')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidteste', 'password': '123456'})
    response = client.get('/gabinete/oficio/')
    assert response.status_code > 400
    cidadao.delete()

@pytest.mark.django_db
def test_deletar_carta_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    carta = Carta()
    carta.save()
    gabinete.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/deletar_carta/1/')
    procurar_carta = gabinete.cartas.filter(id='1')
    assert procurar_carta.count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_gerar_pdf_carta_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    carta = Carta()
    carta.save()
    gabinete.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.get('/gerar_pdf/1/')
    assert response.status_code is 200
    carta.delete()
    organizador.delete()

@pytest.mark.django_db
def test_enviar_carta_email_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'orgteste'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    carta = Carta()
    carta.save()
    gabinete.cartas.add(carta)
    client = Client()
    client.post('/', {'username': 'orgteste', 'password': '123'})
    response = client.post('/enviar_carta/1/', {'email_carta': 'exemplo@teste.com'})
    assert 300 <= response.status_code < 400
    carta.delete()

@pytest.mark.django_db
def test_enviar_oficio_view_post():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.post('/gabinete/oficios/gerar_oficio/', {'remetente': 'Remetente', \
        'destinatario': 'Destinatário', 'forma_tratamento': 'Senhor(a)',\
        'corpo_texto_doc': 'Mensagem'})
    assert 300 <= response.status_code < 400
    organizador.delete()

@pytest.mark.django_db
def test_enviar_oficio_view_post_faltando_campo():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.post('/gabinete/oficios/gerar_oficio/', {'remetente': 'Remetente', \
        'destinatario': 'Destinatário', 'forma_tratamento': 'Senhor(a)',\
        'corpo_texto_doc': ''})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_oficio_view_get_logado():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.get('/gabinete/oficios/')
    assert 300 <= response.status_code < 400
    organizador.delete()

@pytest.mark.django_db
def test_oficio_view_get_deslogado():

    cidadao = Cidadao()
    cidadao.username = 'cidteste'
    cidadao.set_password('123456')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidteste', 'password': '123456'})
    response = client.get('/gabinete/oficios/')
    assert 300 <= response.status_code < 400
    cidadao.delete()

@pytest.mark.django_db
def test_deletar_oficio_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    oficio = Oficio()
    oficio.save()
    gabinete.oficios.add(oficio)
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.get('/deletar_oficio/1/')
    procurar_oficio = gabinete.oficios.filter(id='1')
    assert procurar_oficio.count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_gerar_pdf_oficio_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    oficio = Oficio()
    oficio.save()
    gabinete.oficios.add(oficio)
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.get('/gerar_oficio_pdf/1/')
    assert response.status_code is 200
    oficio.delete()
    organizador.delete()

@pytest.mark.django_db
def test_enviar_oficio_email_view():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'org'
    organizador.set_password('123456')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    oficio = Oficio()
    oficio.save()
    gabinete.oficios.add(oficio)
    client = Client()
    client.post('/', {'username': 'org', 'password': '123456'})
    response = client.post('/enviar_oficio/1/', {'email_oficio': 'exemplo@teste.com'})
    assert 300 <= response.status_code < 400
    oficio.delete()
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_get():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/gabinete/contatos/cadastrar_contato/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    assert gabinete.contatos.get(nome='Contato') is not None
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida1():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-011', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    assert gabinete.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida2():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-012', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    assert gabinete.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida3():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-011'})
    assert gabinete.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_campo_em_branco():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-011', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    assert gabinete.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_excluir_contato_get():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    client.get('/deletar_contato/1/')
    assert gabinete.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_atualizar_contato_get():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/gabinete/contatos/cadastrar_contato/', {'nome': 'Contato', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01'})
    response = client.get('/gabinete/contatos/atualizar_contato/1/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_contato_view_get():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/gabinete/contatos/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_ticket_view_get():

    cidadao = Cidadao()
    cidadao.username = 'cidadao'
    cidadao.set_password('123')
    cidadao.data_de_nascimento = '1900-01-01'
    cidadao.save()
    client = Client()
    client.post('/', {'username': 'cidadao', 'password': '123'})
    response = client.get('/ticket/')
    assert response.status_code is 200
    cidadao.delete()

@pytest.mark.django_db
def test_ticket_view_get_nao_autenticado():

    client = Client()
    response = client.get('/ticket/')
    assert response.status_code is 200

@pytest.mark.django_db
def test_ticket_view_post_anonimo():

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.first_name = 'Organizador'
    organizador.gabinete = gabinete
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.post('/ticket/', {'nome_gabinete': 'Gabinete', \
        'enviar_anonimamente': '', 'assunto': 'Assunto', \
        'descricao': 'Descrição', 'tipo_mensagem': 'Tipo mensagem'})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_view_gabinete():
    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    response = client.get('/gabinete/')

    assert response.status_code is 200
    admin.delete()
    gabinete.delete()

@pytest.mark.django_db
def test_busca_contatos_estado():

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    gabinete.contatos.add(contato);


    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    tipo_busca = "estado"
    pesquisa = 'Sao Paulo'
    response = client.post('/gabinete/contatos/buscar_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()

@pytest.mark.django_db
def test_busca_contatos_genero():

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    gabinete.contatos.add(contato);

    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    tipo_busca = "genero"
    pesquisa = 'Masculino'
    response = client.post('/gabinete/contatos/buscar_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()

@pytest.mark.django_db
def test_busca_contatos_data_aniversario():

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    gabinete.contatos.add(contato);

    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    tipo_busca = "data_de_nascimento"
    pesquisa = '1'
    response = client.post('/gabinete/contatos/buscar_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()

@pytest.mark.django_db
def test_busca_contatos_nome():

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    gabinete.contatos.add(contato);

    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    tipo_busca = "nome"
    pesquisa = 'Maria'
    response = client.post('/gabinete/contatos/buscar_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()

@pytest.mark.django_db
def test_busca_contatos_sem_filtro():

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()
    gabinete.contatos.add(contato);

    client = Client()
    client.post('/', {'username': 'administrador', 'password': '123'})
    tipo_busca = ""
    pesquisa = 'sabino'
    response = client.post('/gabinete/contatos/buscar_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()

@pytest.mark.django_db
def test_criar_grupo_de_contatos():

    client=Client()

    banco_antes = Grupo.objects.all().count()
    teste_nome_grupo = 'brasileiros'

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()

    client.post('/', {'username': 'administrador', 'password': '123'})
    client.post('/criar_grupo/',{'nome_grupo':teste_nome_grupo})

    banco_depois = Grupo.objects.all().count()

    assert banco_depois > banco_antes
    Grupo.objects.all().last().delete()


@pytest.mark.django_db
def test_adiciona_contato_ao_grupo():

    client = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = "Gabinete"
    gabinete.save()
    admin = AdministradorGabinete()
    admin.username = 'administrador'
    admin.set_password('123')
    admin.data_de_nascimento = '1900-01-01'
    admin.gabinete = gabinete
    admin.save()

    client.post('/', {'username': 'administrador', 'password': '123'})
    teste_nome_grupo = 'teste_grupo_teste'
    client.post('/criar_grupo/',{'nome_grupo':teste_nome_grupo})

    contato = Contato()
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Osasco'
    contato.cep = '72000000'
    contato.estado = 'Sao Paulo'
    contato.email = "teste@teste.com"
    contato.save()

    gabinete.contatos.add(contato);

    contato = Contato.objects.all().last()
    grupo_novo = Grupo.objects.all().last()

    client.post('/adicionar_contatos/',{'contatos': contato.id,'nome_grupo':teste_nome_grupo})

    assert grupo_novo.contatos.all().count() == 1


def test_busca_contatos_cidade():

    client = Client()
    tipo_busca = "cidade"
    pesquisa = 'df'
    response = client.post('gabinete/contatos/buscar_contatos/?tipo_busca=%s&pesquisa=%s',tipo_busca,pesquisa)
