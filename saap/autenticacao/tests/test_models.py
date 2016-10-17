# coding=utf-8
from autenticacao.models import *
import pytest
# Create your tests here.



@pytest.mark.django_db
def test_busca_nome():
    u = Usuario_saap()
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

    users_test = Usuario_saap.busca_nome(u.first_name)
    assert u in users_test
    u.delete()

@pytest.mark.django_db
def test_deleta_usuario():
    u = Usuario_saap()
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
def test_busca_username():

    u = Usuario_saap()
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
    verifica_user = Usuario_saap.busca_username('test_name')

    assert verifica_user.count() > 0
    u.delete() #Essa linha não vai executar ...


@pytest.mark.django_db
def test_criar_vereador():

    ver = Usuario_saap.busca_username('vereadorteste')
    if ver.count() >= 1:
        ver[1].delete()

    vereador = OrganizadorGabinete()
    vereador.first_name = 'Vereador'
    vereador.last_name = 'Tal'
    vereador.username = 'vereadorteste'
    vereador.email = 'email@example.com'
    vereador.set_password('12345678')
    vereador.data_de_nascimento = '1990-10-10'
    vereador.sexo = 'Masculino'
    vereador.municipio = 'Brasilia'
    vereador.uf = 'DF'
    vereador.gabinete = Gabinete_saap()
    vereador.save()

    verificador = Usuario_saap.busca_username('vereadorteste')

    assert verificador.count() == 1

@pytest.mark.django_db
def test_deletar_vereador():

        ver = Usuario_saap.busca_username('vereadorteste')
        if ver.count() >= 1:
            ver[1].delete()
            ver = Usuario_saap.busca_username('vereadorteste')
            assert ver.count() == 0
        else:
            vereador = OrganizadorGabinete()
            vereador.first_name = 'Vereador'
            vereador.last_name = 'Tal'
            vereador.username = 'vereadorteste'
            vereador.email = 'email@example.com'
            vereador.set_password('12345678')
            vereador.data_de_nascimento = '1990-10-10'
            vereador.sexo = 'Masculino'
            vereador.municipio = 'Brasilia'
            vereador.uf = 'DF'
            vereador.gabinete = Gabinete_saap()
            vereador.save()

            ver = Usuario_saap.busca_username('vereadorteste')

            if ver.count() == 1:
                vereador.delete()
                ver = Usuario_saap.busca_username('vereadorteste')

                assert ver.count() == 0
            else:
                #Commit again
                self.fail('TEST_ERROR: UNABLE TO DELETE VEREADOR')
