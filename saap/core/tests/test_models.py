from core.models import Ticket, Carta
from autenticacao.models import *
from core.models import *
from django.test import Client
import pytest
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_public_view_ticket():
    c = Client()
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

    organizador.save()

    c.login(username='organizador',password='123456')

    response= {'envio_anonimo': 'Anonimo',
              'enviar_anonimamente': 'True',
              'descricao': 'Rua com burracos',
              'assunto':'blablabla',
              'tipo_mensagem':'oioioioioi',
              'nome_organizador':"contato"}

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

@pytest.mark.django_db
def test_deleta_organizador_gabinete():
    u = OrganizadorGabinete()
    u.first_name = 'test_name'
    u.last_name = 'test_last'
    u.username = 'test_name'
    u.email = 'test@email.com'
    u.set_password('123')
    u.data_de_nascimento = '1990-10-10'
    u.sexo = 'Masculino'
    u.municipio = 'Brasilia'
    u.uf = 'DF'
    u.save()
    db_before = Usuario_saap.objects.get(pk=1)

    Usuario_saap.deleta_usuario(1)
    db_after = Usuario_saap.objects.all()
    # db_before.count() > db_after.count()
    assert db_before is not \
    None and db_after.count() is 0

@pytest.mark.django_db
def test_cria_oficio():
    oficio = Oficio()
    oficio.tipo_documento = 'Carta'
    oficio.remetente = 'email@email.com'
    oficio.destinatario = 'exemplo@email.com'
    oficio.titulo_documento = 'Titulo Exemplo'
    oficio.corpo_texto_doc = 'Texto enviado para email por exemplos'
    oficio.data = '24/10/2016'
    oficio.save()

    busca = Oficio.busca_por_titulo('Titulo Exemplo')

    assert busca.count() >= 1

@pytest.mark.django_db
def test_deleta_oficio():

    busca = Oficio.busca_por_titulo('Titulo Exemplo')
    if busca.count() < 1:
        oficio = Oficio()
        oficio.tipo_documento = 'Carta'
        oficio.remetente = 'email@email.com'
        oficio.destinatario = 'exemplo@email.com'
        oficio.titulo_documento = 'Titulo Exemplo'
        oficio.corpo_texto_doc = 'Texto enviado para email por exemplos'
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
def test_model_adminGabinete():

    adminGabinete = AdminGabinete()

    adminGabinete.nome_admin = 'nome_teste'
    adminGabinete.enderecoCasa = 'enderecoCasa_teste'
    adminGabinete.enderecoGabinete = 'enderecoGabinete_teste'
    adminGabinete.emailCorporativo = 'emailCorporativo@teste.com'
    adminGabinete.logoCasa = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

    adminGabinete.save()

    assert adminGabinete >= 1
    adminGabinete.delete()
