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
    
    def get(self, request):
        if request.user.is_authenticated():
            response = redirect('/')
        else:
            response = render(request, 'cadastro.html')
        return response
    
    def post(self, request):

        if (request.POST['first_name'] and request.POST['last_name'] and 
            request.POST['username'] and request.POST['email'] and 
            request.POST['confirmacao_email'] and request.POST['password'] and
            request.POST['confirmacao_password'] and 
            request.POST['data_de_nascimento'] and request.POST['sexo'] and 
            request.POST['municipio']) is not None:
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
        return response
