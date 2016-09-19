from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext
from core.models import Contato

class CadastroView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'cadastro_contato.html')
        return response

    def validacao (self, arg):
        if arg is not "":
            return True
        else:
            return False

    def campo_vazio(self,campos):
        for campo in campos:
            if campo is not "":
                return True
            else:
                return False

    def post (self,request):
        campos = [request.POST['nome'],request.POST['data_de_nascimento'],
        request.POST['sexo'],request.POST['telefone'], request.POST['celular'],
        request.POST['fax'], request.POST['cpf'], request.POST['rg'], request.POST['endereco'],
        request.POST['cidade'], request.POST['cep'], request.POST['estado'], request.POST['email'],
        request.POST['grupo'], request.POST['titulo']]

        if self.campo_vazio(campos) :

            nome = request.POST['nome']
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            telefone = request.POST['telefone']
            celular = request.POST['celular']
            fax = request.POST['fax']
            cpf = request.POST['cpf']
            rg= request.POST['rg']
            endereco = request.POST['endereco']
            cidade = request.POST['cidade']
            cep = request.POST['cep']
            estado = request.POST['estado']
            email = request.POST['email']
            grupo = request.POST['grupo']
            titulo = request.POST['titulo']

            contato = Contato()
            contato.nome = nome
            contato.data_de_nascimento = data_de_nascimento
            contato.sexo = sexo
            contato.telefone = telefone
            contato.celular = celular
            contato.fax = fax
            contato.cpf = cpf
            contato.rg= rg
            contato.endereco = endereco
            contato.cidade = cidade
            contato.cep = cep
            contato.estado = estado
            contato.email = email
            contato.grupo = grupo
            contato.titulo = titulo
            contato.save()
            response = render (request, 'contato.html')
        else:
            messages.error(request,'Preencha todos os campos!')

        return response

class DeletarContatoView(View):
    http_method_names = [u'get',u'post']

    def get (self, request):
        response = render(request, 'exclui_contato.html')
        return response

    def post(self, request):
        busca_nome = request.POST['busca_nome']
        c = Contato.objects.filter(nome = busca_nome)
        c.delete()
        response = render(request,'cadastro_contato.html')
        return response

class ContatoView(View):
    http_method_names = [u'get', u'post']

    def get (self, request):
        contatos = Contato.objects.all()
        lista_contatos = list(contatos)
        return render(request,'contato.html',locals())
