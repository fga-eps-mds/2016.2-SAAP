# coding=utf-8
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import RequestContext
from autenticacao.models import Cidadao, OrganizadorContatos
from django.utils.translation import ugettext
from default.views import *
from core.views import (ContatoView)
from django.contrib.auth.decorators import login_required

def checar_autenticacao(request, resposta_autenticado, resposta_nao_autenticado):
    if request.user.is_authenticated():
        resposta = resposta_autenticado
    else:
        resposta = render(request, resposta_nao_autenticado)
    return resposta

def checar_confirmacao(atributo, confirmacao_atributo):
    if atributo == confirmacao_atributo:
        return True
    else:
        return False

def checar_tipo_usuario(request, username):
    try:
        tipo_usuario = Cidadao.objects.get(username=username)
    except:
        tipo_usuario = None
    if tipo_usuario.__class__ is Cidadao:
        return render(request, 'perfil.html')

    try:
        tipo_usuario = OrganizadorContatos.objects.get(username=username)
    except:
        tipo_usuario = None
    if tipo_usuario.__class__ is OrganizadorContatos:
        return render_contatos_tickets(request)

class LoginView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        resposta = checar_autenticacao(request, checar_tipo_usuario(request, request.user.username), 'login.html')
        return resposta

    def post(self, request):

        data = {}
        data['username'] = request.POST['username']

        campos_validados = checar_campos([request.POST['username'], \
            request.POST['password']])

        if campos_validados is True:

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return checar_tipo_usuario(request, username)
                else:
                    messages.error(request, 'Conta desativada!')
            else:
                messages.error(request, 'Nome de usuário e/ou senha inválido(s)!')
        else:
            messages.error(request, 'O campo "%s" não foi preenchido!' % \
                campos_login[campos_validados])

        return render(request, 'login.html', {'data':data})


class RegistroCidadaoView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        resposta = checar_autenticacao(request, 'perfil.html', 'cadastro.html')
        return resposta

    def post(self, request):

        data['first_name'] = request.POST['first_name']
        data['last_name'] = request.POST['last_name']
        data['username'] = request.POST['username']
        data['email'] = request.POST['email']
        data['confirmacao_email'] = request.POST['confirmacao_email']
        data['data_de_nascimento'] = request.POST['data_de_nascimento']
        data['sexo'] = request.POST['sexo']
        data['municipio'] = request.POST['municipio']
        data['uf'] = request.POST['uf']

        campos_validados = checar_campos_registro(request)

        if campos_validados is True:

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = checar_confirmacao(request.POST['email'], request.POST['confirmacao_email'])
            if email is True:
                email = request.POST['email']
            else:
                return render_mensagem_erro(request, 'O e-mail informado é \
                    diferente da confirmação de e-mail! Digite novamente.', \
                    'cadastro.html', {'data':data})
            password = checar_confirmacao(request.POST['password'], request.POST['confirmacao_password'])
            if password is True:
                password = request.POST['password']
            else:
                return render_mensagem_erro(request, 'A senha informada é \
                    diferente da confirmação de senha! Digite novamente.', \
                    'cadastro.html', {'data':data})
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            municipio = request.POST['municipio']
            uf = request.POST['uf']

            if checar_data(data_de_nascimento) :

                if Cidadao.get_usuario_por_username(username).count() == 0 and \
                    OrganizadorContatos.get_usuario_por_username(username).count() == 0:
                    user = Cidadao()
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.email = email
                    user.set_password(password)
                    user.data_de_nascimento = data_de_nascimento
                    user.sexo = sexo
                    user.municipio = municipio
                    user.uf = uf
                    user.save()
                    login(request, user)
                    response = render(request, 'perfil.html')
                else:
                    response = render_mensagem_erro(request, 'Já existe um \
                        usuário com esse "Nome de Usuário"!', 'cadastro.html', {'data':data})
            else:
                response = render_mensagem_erro(request, 'Formato de data \
                    inválido (AAAA-MM-DD)!', 'cadastro.html', {'data':data})
        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_cadastro[campos_validados], \
                'cadastro.html', {'data':data})

        return response

class RegistroOrganizadorView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        resposta = render(request, 'criar_organizador.html')
        return resposta

    def post(self, request):

        data['first_name'] = request.POST['first_name']
        data['last_name'] = request.POST['last_name']
        data['username'] = request.POST['username']
        data['email'] = request.POST['email']
        data['confirmacao_email'] = request.POST['confirmacao_email']
        data['data_de_nascimento'] = request.POST['data_de_nascimento']
        data['sexo'] = request.POST['sexo']
        data['municipio'] = request.POST['municipio']
        data['uf'] = request.POST['uf']

        campos_validados = checar_campos_registro(request)

        if campos_validados is True:

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = checar_confirmacao(request.POST['email'], request.POST['confirmacao_email'])
            if email is True:
                email = request.POST['email']
            else:
                return render_mensagem_erro(request, 'O e-mail informado é \
                    diferente da confirmação de e-mail! Digite novamente.', \
                    'criar_organizador.html', {'data':data})
            password = checar_confirmacao(request.POST['password'], request.POST['confirmacao_password'])
            if password is True:
                password = request.POST['password']
            else:
                return render_mensagem_erro(request, 'A senha informada é \
                    diferente da confirmação de senha! Digite novamente.', \
                    'criar_organizador.html', {'data':data})
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            municipio = request.POST['municipio']
            uf = request.POST['uf']

            if checar_data(data_de_nascimento) :

                if Cidadao.get_usuario_por_username(username).count() == 0 and \
                    OrganizadorContatos.get_usuario_por_username(username).count() == 0:
                    user = OrganizadorContatos()
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.email = email
                    user.set_password(password)
                    user.data_de_nascimento = data_de_nascimento
                    user.sexo = sexo
                    user.municipio = municipio
                    user.uf = uf
                    user.save()
                    response = render(request, 'login.html')
                else:
                    response = render_mensagem_erro(request, 'Já existe um \
                        usuário com esse "Nome de Usuário"!', 'criar_organizador.html', {'data':data})
            else:
                response = render_mensagem_erro(request, 'Formato de data \
                    inválido (AAAA-MM-DD)!', 'criar_organizador.html', {'data':data})
        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_cadastro[campos_validados], \
                'criar_organizador.html', {'data':data})

        return response

class PerfilView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        resposta = checar_autenticacao(request, 'perfil.html', 'login.html')
        return resposta

class LogoutView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        logout(request)
        response = render(request, 'login.html')
        return response

class MudarSenhaView(View):
    http_method_names = [u'get',u'post']

    def get(self, request):
        response = render (request, 'mudar_senha.html')
        return response

    def post(self,request):

        data = {}
        data['nova_senha'] = request.POST['nova_senha']
        data['confirmacao_nova_senha'] = request.POST['confirmacao_nova_senha']

        campos_validados = checar_campos([request.POST['nova_senha'], \
            request.POST['confirmacao_nova_senha']])

        if campos_validados is True:

            user = request.user
            username = user.username
            nova_senha = request.POST['nova_senha']
            nova_senha2 = request.POST['confirmacao_nova_senha']

            if nova_senha == nova_senha2:
                user.set_password(nova_senha)
                user.save()
                user = authenticate(username=username, password=nova_senha)
                login(request, user)
                response = render(request, 'perfil.html')
            else:
                messages.error(request, 'As senhas não são iguais! \
                    Digite novamente.')
                response = render(request, 'mudar_senha.html')

        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_mudar_senha[campos_validados], \
                'mudar_senha.html', {'data':data})

        return response

class ExcluirContaView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'excluir_conta.html')
        return response

    def post(self, request):

        data = {}
        data['password'] = request.POST['password']

        campos_validados = checar_campos([request.POST['password']])

        password = request.POST['password']
        user = authenticate(username=request.user.username, password=password)

        if campos_validados is True:

            if user is not None:
                user.delete()
                messages.success(request, 'Sua conta foi excluída')
                response = render(request, 'login.html')
                return response
            else:
                response = render_mensagem_erro(request, 'Senha incorreta! \
                    Digite novamente.', 'excluir_conta.html', {'data':data})
        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_excluir_conta[campos_validados], \
                'excluir_conta.html', {'data':data})

        return response
