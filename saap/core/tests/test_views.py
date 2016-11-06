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
def test_enviar_ticket_campo_em_branco():
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

    organizador = OrganizadorContatos()

    organizador.username = 'sabino'
    organizador.first_name = 'sabino'
    organizador.data_de_nascimento = '1990-01-01'
    organizador.sexo = 'masculino'
    organizador.municipio = 'ceilandia'
    organizador.uf = 'df'
    organizador.set_password('eusoueu0')

    organizador.save()

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

    assert tickets == 0

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

@pytest.mark.django_db
def test_cadastro_contato_get():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/cadastro_contato/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    assert organizador.contatos.get(nome='Contato') is not None
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida1():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    assert organizador.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida2():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    assert organizador.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_data_invalida3():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    assert organizador.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_cadastro_contato_post_campo_em_branco():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    assert organizador.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_excluir_contato_get():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/exclui_contato/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_excluir_contato_post():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato', \
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
    client.post('/exclui_contato/', {'busca_email': 'teste@teste.com'})
    assert organizador.contatos.filter(nome='Contato').count() == 0
    organizador.delete()

@pytest.mark.django_db
def test_excluir_contato_post_contato_inexistente():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.post('/exclui_contato/', {'busca_email': 'teste@teste.com'})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_atualizar_contato_get():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/atualiza_contato/')
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_atualizar_contato_post():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato1', \
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
    client.post('/atualiza_contato/', {'nome': 'Contato2', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '12345678912', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01', \
        'busca_email': 'teste@teste.com'})
    assert organizador.contatos.get(nome='Contato2') is not None
    organizador.delete()

@pytest.mark.django_db
def test_atualizar_contato_post_campo_em_branco():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    client.post('/cadastro_contato/', {'nome': 'Contato1', \
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
    client.post('/atualiza_contato/', {'nome': 'Contato2', \
        'data_de_nascimento': '1900-01-01', 'telefone': '61-9111-1111', \
        'sexo': 'Masculino', 'celular': '61-9111-1111', 'cpf': '', \
        'fax': '61-9111-1111', 'rg': '12345678', 'endereco': 'Endereço', \
        'cidade': 'Cidade', 'estado': 'Estado', 'cep': '72000000', \
        'email': 'teste@teste.com', 'grupo': 'Grupo 1', 'titulo': 'Senhor(a)', \
        'titulo_de_eleitor': '123123', 'profissao': 'Profissão', \
        'zona': '123', 'cargo': 'Cargo', 'secao': '123', 'empresa': 'Empresa', \
        'dependente_nome': 'Dependente', 'dependente_aniversario': '1900-01-01', \
        'dependente_parentesco': 'Parentesco', \
        'dependente_partido': 'Partido', 'dependente_data_filiacao': '1900-01-01', \
        'busca_email': 'teste@teste.com'})
    assert organizador.contatos.get(nome='Contato1') is not None
    organizador.delete()

@pytest.mark.django_db
def test_contato_view_get():

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.get('/contato/')
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

    organizador = OrganizadorContatos()
    organizador.username = 'organizador'
    organizador.set_password('123')
    organizador.data_de_nascimento = '1900-01-01'
    organizador.first_name = 'Organizador'
    organizador.save()
    client = Client()
    client.post('/', {'username': 'organizador', 'password': '123'})
    response = client.post('/ticket/', {'nome_organizador': 'Organizador', \
        'enviar_anonimamente': '', 'assunto': 'Assunto', \
        'descricao': 'Descrição', 'tipo_mensagem': 'Tipo mensagem'})
    assert response.status_code is 200
    organizador.delete()

@pytest.mark.django_db
def test_busca_contatos_cidade():

    contato = Contato() 
    contato.nome = 'teste'
    contato.data_de_nascimento='1990-01-01'
    contato.sexo = 'Masculino'
    contato.endereco = 'Qnl 29 teste casa teste 20'
    contato.cidade = 'Taguatinga'
    contato.cep = '72000000'
    contato.estado = 'DF'
    contato.email = "teste@teste.com"
    contato.save()


    client = Client()
    tipo_busca = "cidade"
    pesquisa = 'df'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete()


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


    client = Client()
    tipo_busca = "estado"
    pesquisa = 'Sao Paulo'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

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


    client = Client()
    tipo_busca = "genero"
    pesquisa = 'Masculino'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

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


    client = Client()
    tipo_busca = "data_de_nascimento"
    pesquisa = '1'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

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


    client = Client()
    tipo_busca = "Data_aniversario"
    pesquisa = '1'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

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


    client = Client()
    tipo_busca = "nome"
    pesquisa = 'Maria'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

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


    client = Client()
    tipo_busca = ""
    pesquisa = 'sabino'
    response = client.post('/busca_contatos/',{'tipo_busca':tipo_busca,'pesquisa':pesquisa})

    assert response.status_code == 200
    contato.delete() 

@pytest.mark.django_db
def test_criar_grupo_de_contatos():

    client=Client()

    banco_antes = Grupo.objects.all().count()
    teste_nome_grupo = 'brasileiros'

    client.post('/criar_grupo/',{'nome_grupo':teste_nome_grupo})

    banco_depois = Grupo.objects.all().count()

    assert banco_depois > banco_antes
    Grupo.objects.all().last().delete()


@pytest.mark.django_db
def test_adiciona_contato_ao_grupo():

    client = Client()

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
        
    contato = Contato.objects.all().last()
    grupo_novo = Grupo.objects.all().last()

    client.post('/adicionar_contatos/',{'contatos': contato.id,'nome_grupo':teste_nome_grupo})
    
    assert grupo_novo.contatos.all().count() == 1

