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
        return atributo

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
            messages.success(request, 'Nome de usuário e/ou senha inválido(s)!')

        return render(request, 'login.html')


class RegistroView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.path == '/cadastro/':
            resposta = checar_autenticacao(request, 'perfil.html', 'cadastro.html')
        elif request.path == '/criar_organizador/':
            resposta = render(request, 'criar_organizador.html')
        return resposta

    def post(self, request):

        campos = [request.POST['first_name'], request.POST['last_name'], \
            request.POST['username'], request.POST['email'], \
            request.POST['confirmacao_email'], request.POST['password'], \
            request.POST['confirmacao_password'], request.POST['sexo'], \
            request.POST['municipio'], request.POST['uf'], \
            request.POST['data_de_nascimento']]

        if checar_vazio(campos):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = checar_confirmacao(request.POST['email'], request.POST['confirmacao_email'])
            password = checar_confirmacao(request.POST['password'], request.POST['confirmacao_password'])
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            municipio = request.POST['municipio']
            uf = request.POST['uf']

            if Cidadao.get_usuario_por_username(username).count() == 0 and \
                OrganizadorContatos.get_usuario_por_username(username).count() == 0:
                if request.path == '/cadastro/':
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
                response = redirect('/erroCadastro')
        else:
            response = redirect('/erroCadastroCampoVazio')

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
        user = request.user
        nova_senha = request.POST['nova_senha']
        nova_senha2 = request.POST['confirmacao_nova_senha']

        if nova_senha == nova_senha2:
            user.set_password(nova_senha)
            user.save()
        else:
            messages.error(request, 'As senhas não são iguais! Digite novamente.')
            return render(request, 'mudar_senha.html')

        return render(request, 'perfil.html')

class ExcluirContaView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'excluir_conta.html')
        return response

    def post(self, request):
        password = request.POST['password']
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            user.delete()
            messages.success(request, 'Sua conta foi excluída')
            response = render(request, 'login.html')
            return response
        else:
            messages.error(request, 'Senha incorreta')
            return render(request, 'excluir_conta.html')
