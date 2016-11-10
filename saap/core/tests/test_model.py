#coding=utf-8

import pytest
from django.test import Client
from core.models import Grupo,Contato


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


	pesquisa = Grupo.filtro_nascimento(mes_do_ano='01')[0]
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
