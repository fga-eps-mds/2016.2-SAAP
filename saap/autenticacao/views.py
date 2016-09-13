# coding=utf-8
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import RequestContext
from autenticacao.models import Usuario_saap
from django.utils.translation import ugettext
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
"""from django.core.mail import send_mail
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from reset_password.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from utils.forms import PasswordResetRequestForm, SetPasswordForm"""

# Create your views here.


class LoginView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            response = render(request, 'perfil.html')
        else:
            response = render(request, 'login.html')
        return response

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'perfil.html')
            else:
                messages.error(request, 'Conta desativada!')
        else:
            messages.success(request, 'Nome de usuário e/ou senha inválido(s)!')

        return render(request, 'login.html')


class RegistroView(View):
    http_method_names = [u'get', u'post']

    def valido(self, arg):
        if arg is not "":
            return True
        else:
            return False

    def get(self, request):
        if request.user.is_authenticated():
            response = render(request, 'perfil.html')
        else:
            response = render(request, 'cadastro.html')
        return response

    def post(self, request):

        print("%s", request.POST['data_de_nascimento'])
        first_name = ""
        last_name = ""
        username = ""
        email = ""
        confirmacao_email = ""
        password = ""
        confirmacao_password = ""
        sexo =  ""
        municipio = ""
        uf = ""
        data_de_nascimento = "1900-01-01"

        if self.valido(request.POST['first_name']) and \
            self.valido(request.POST['last_name']) and \
            self.valido(request.POST['username']) and \
            self.valido(request.POST['email']) and \
            self.valido(request.POST['confirmacao_email']) and \
            self.valido(request.POST['password']) and \
            self.valido(request.POST['confirmacao_password']) and \
            self.valido(request.POST['sexo']) and \
            self.valido(request.POST['municipio']) and \
            self.valido(request.POST['uf']) and \
            self.valido(request.POST['data_de_nascimento']):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            if request.POST['email'] == request.POST['confirmacao_email']:
                email = request.POST['email']
            if request.POST['password'] == request.POST['confirmacao_password']:
                password = request.POST['password']
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            municipio = request.POST['municipio']
            uf = request.POST['uf']
        else:
            response = redirect('/erroCadastro')

        if Usuario_saap.get_usuario_por_username(username).count() == 0:
            user = Usuario_saap()
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
            response = redirect('/erroCadastro')

        return response

class PerfilView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            response = render(request, 'perfil.html')
        else:
            response = render(request, 'login.html')
        return response

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
