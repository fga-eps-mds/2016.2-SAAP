# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (LoginView, MudarSenhaView, RegistroView, PerfilView, LogoutView)


urlpatterns = [
    url(r'^$', LoginView.as_view(),
        name='login'),
    url(r'^login/$', LoginView.as_view(),
        name='login'),
    url(r'^cadastro/$', RegistroView.as_view(),
        name='cadastro'),
    url(r'^perfil/$', login_required(PerfilView.as_view()),
        name='perfil'),
    url(r'^logout/$', login_required(LogoutView.as_view()),
        name='logout'),
    url(r'^mudar_senha/$', login_required(MudarSenhaView.as_view()),
        name='mudar_senha'),

]
