from autenticacao.models import *
from core.models import *
import pytest

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
