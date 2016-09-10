# coding=utf-8
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from autenticacao.models import Usuario_saap


class LoginView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            response = redirect('/')
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
                return redirect('/logado')
            else:
                messages.error(request, 'Conta desativada!')
                return redirect('/contaDesativada')
        else:
            messages.success(request, 'Nome de usuário e/ou senha inválido(s)!')
            return redirect('/usuarioInvalido')
            
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
            response = redirect('/')
        else:
            response = render(request, 'cadastro.html')
        return response

    def post(self, request):

        first_name = ""
        last_name = ""
        username = ""
        email = ""
        confirmacao_email = ""
        password = ""
        confirmacao_password = ""
        sexo =  ""
        municipio = ""
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
            data_de_nascimento is not None:
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
            user.save()
            login(request, user)
            response = redirect('/registrado')
        else:
            response = redirect('/erroRegistro')
        return response
