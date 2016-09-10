# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext


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
                return redirect('/')
            else:
                messages.error(request, 'Conta desativada!')
        else:
            messages.success(request, 'Nome de usuário e/ou senha inválido(s)!')
        
        return render(request, 'login.html')
