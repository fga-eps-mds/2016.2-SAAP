from core.models import Ticket, Carta
from autenticacao.models import *
from core.models import *
from django.test import Client
import pytest
from django.test import Client

@pytest.mark.django_db
def test_public_view_ticket():
    c = Client()

    gabinete = Gabinete()
    gabinete.nome_gabinete = 'Gabinete'
    gabinete.save()

    organizador = OrganizadorContatos()

    organizador.username = 'organizador'
    organizador.first_name = 'contato'
    organizador.data_de_nascimento = '2016-10-15'
    organizador.username = 'organizador'
    organizador.email = 'organizador@email.com'
    organizador.set_password('123456')
    organizador.sexo = 'masculino'
    organizador.municipio = 'Brasilia'
    organizador.uf = 'DF'
    organizador.gabinete = gabinete

    organizador.save()

    c.login(username='organizador',password='123456')

    response= {'envio_anonimo': 'Anonimo',
              'enviar_anonimamente': 'True',
              'descricao': 'Rua com burracos',
              'assunto':'blablabla',
              'tipo_mensagem':'oioioioioi',
              'nome_gabinete':'Gabinete'}

    c.post('/ticket/', response)

    ticket = Ticket.objects.all()[0]
    response= {'ticket_id': ticket.id}

    retorno = c.post('/publicar_ticket/', response,follow=True)

    assert retorno.status_code == 200

@pytest.mark.django_db
def test_model_carta():

    carta = Carta()

    carta.nome_remetente = 'nome_teste1'
    carta.nome_destinatario = 'nome_teste2'
    carta.data = '2016-10-23'
    carta.local = 'local_teste'
    carta.assunto = 'assunto_teste'
    carta.texto = 'texto_teste'

    carta.save()
    cartas = Carta.objects.all().count()

    assert cartas >= 1
    carta.delete()

# @pytest.mark.django_db
# def test_deleta_organizador_gabinete():
#     u = OrganizadorGabinete()
#     u.first_name = 'test_name'
#     u.last_name = 'test_last'
#     u.username = 'test_name'
#     u.email = 'test@email.com'
#     u.set_password('123')
#     u.data_de_nascimento = '1990-10-10'
#     u.sexo = 'Masculino'
#     u.municipio = 'Brasilia'
#     u.uf = 'DF'
#     u.save()
#     db_before = Usuario_saap.objects.get(pk=1)
#
#     Usuario_saap.deleta_usuario(1)
#     db_after = Usuario_saap.objects.all()
#     # db_before.count() > db_after.count()
#     assert db_before is not \
#     None and db_after.count() is 0

@pytest.mark.django_db
def test_cria_oficio():
    oficio = Oficio()
    oficio.remetente = 'email@email.com'
    oficio.destinatario = 'exemplo@email.com'
    oficio.titulo_documento = 'Titulo Exemplo'
    oficio.corpo_texto_doc = 'Texto enviado para email por exemplos'
    oficio.forma_tratamento = 'Senhor'
    oficio.data = '24/10/2016'
    oficio.save()

    busca = Oficio.busca_por_titulo('Titulo Exemplo')

    assert busca.count() >= 1

@pytest.mark.django_db
def test_deleta_oficio():

    busca = Oficio.busca_por_titulo('Titulo Exemplo')
    if busca.count() < 1:
        oficio = Oficio()
        oficio.remetente = 'email@email.com'
        oficio.destinatario = 'exemplo@email.com'
        oficio.titulo_documento = 'Titulo Exemplo'
        oficio.corpo_texto_doc = 'Texto enviado para email por exemplos'
        oficio.forma_tratamento = 'Senhor'
        oficio.data = '24/10/2016'
        oficio.save()

        busca = Oficio.busca_por_titulo(oficio.titulo_documento)

        if busca.count() == 1:
            busca[0].delete()

    else:
        busca[0].delete()
        #endif

    busca = Oficio.busca_por_titulo('Titulo Exemplo')
    assert busca.count() == 0

@pytest.mark.django_db
def test_model_carta():

    carta = Carta()

    carta.nome_remetente = 'nome_teste1'
    carta.nome_destinatario = 'nome_teste2'
    carta.data = '2016-10-23'
    carta.local = 'local_teste'
    carta.assunto = 'assunto_teste'
    carta.texto = 'texto_teste'

    carta.save()
    cartas = Carta.objects.all().count()

    assert cartas >= 1
    carta.delete()

@pytest.mark.django_db
def test_grupo_Creation():

	before = Grupo.objects.all().count()

	grupo = Grupo()
	grupo.nome = 'brasileiros'
	grupo.save()

	after = Grupo.objects.all().count()

	assert before < after


@pytest.mark.django_db
def test_str_method():

	grupo = Grupo()
	grupo.nome = "Brasileiros"

	grupo.save()

	assert "Brasileiros" is grupo.__str__()
	grupo.delete()

@pytest.mark.django_db
def test_filtro_nascimento():

	grupo = Grupo()
	grupo.nome = 'teste-grupo'
	grupo.save()


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

	contato.grupo.add(grupo)
	contato.save()


	pesquisa = Grupo.filtro_data_aniversario(mes_do_ano='01')[0]
	c = pesquisa.contatos.get()
	assert str(c.data_de_nascimento.isoformat()) == contato.data_de_nascimento
	grupo.delete()
	contato.delete()

@pytest.mark.django_db
def test_filtro_cidade():

	grupo = Grupo()
	grupo.nome = 'teste-grupo'
	grupo.save()


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

	contato.grupo.add(grupo)
	contato.save()


	pesquisa = Grupo.filtro_cidade(cidade='Taguatinga')[0]
	c = pesquisa.contatos.get()
	assert c.cidade == contato.cidade
	grupo.delete()
	contato.delete()

@pytest.mark.django_db
def test_filtro_genero():

	grupo = Grupo()
	grupo.nome = 'teste-grupo'
	grupo.save()

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

	contato.grupo.add(grupo)
	contato.save()


	pesquisa = Grupo.filtro_genero(sexo=contato.sexo)
	c = pesquisa[0].contatos.get()
	assert c.sexo == contato.sexo
	grupo.delete()
	contato.delete()
