# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (LoginView, MudarSenhaView, RegistroCidadaoView, PerfilView,
                    LogoutView, ExcluirContaView, RegistroOrganizadorView,
                    RegistroAdminSisView, RegistroAdministradorView)


urlpatterns = [
    url(r'^$', LoginView.as_view(),
        name='login'),
    url(r'^login/$', LoginView.as_view(),
        name='login'),
    url(r'^cadastro/$', RegistroCidadaoView.as_view(),
        name='cadastro'),
    url(r'^perfil/$', login_required(PerfilView.as_view()),
        name='perfil'),
    url(r'^logout/$', login_required(LogoutView.as_view()),
        name='logout'),
    url(r'^mudar_senha/$', login_required(MudarSenhaView.as_view()),
        name='mudar_senha'),
    url(r'^excluir_conta/$', login_required(ExcluirContaView.as_view()),
        name='excluir_conta'),
    url(r'^gabinete/criar_organizador/$', login_required(RegistroOrganizadorView.as_view()),
        name='criar_organizador'),
    url(r'^criar_administrador/$', RegistroAdministradorView.as_view(),
            name='criar_administrador'),
    url(r'^criar_adm_sis/$', login_required(RegistroAdminSisView.as_view()),
        name='criar_adm_sis'),
]
