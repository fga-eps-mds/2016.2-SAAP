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
from autenticacao.models import Usuario_saap
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
from django.contrib import messages



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

"""

class ResetPasswordRequestView(FormView):
    # code for template is given below the view's code
    template_name = "recuperacao_senha.html"
    success_url = '/admin/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'your site',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'recuperacao_senha.html'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_subject.txt
        # to templates directory
        email_template_name = 'recuperacao_senha.html'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_email.html
        # to templates directory
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data["email_or_username"]
            # uses the method written above
            if self.validate_email_address(data) is True:

                associated_users = User.objects.filter(
                    Q(email=data) | Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        self.reset_password(user, request)

                    result = self.form_valid(form)
                    messages.success(
                        request, 'Um email foi enviado para {0}. Por favor checar sua caixa de mensagem para continuar redefinindo sua senha.'.format(data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'Nenhum usuario esta cadastrado com esse email.')
                return result
            else:
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        self.reset_password(user, request)
                    result = self.form_valid(form)
                    messages.success(
                        request, "Um email foi enviado para {0} endereço de email. Por favor confira sua caixa de mensagem para prosseguir redefinindo sua senha.".format(data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'Usuário não cadastrado no sistema.')
                return result
            messages.error(request, 'Entrada inválida')
        except Exception as e:
            print(e)
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "recuperacao_senha.html"
    success_url = '/admin/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):

        Usuario_saap = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = Usuario_saap._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario_saap.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Sua senha foi redefinida com sucesso!')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Redefinição de senha não bem sucedida.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'Esse link de refedinição de senha não é mais válido')
            return self.form_invalid(form)"""
