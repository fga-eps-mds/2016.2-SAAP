# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (LoginView, RegistroView, PerfilView, LogoutView)
"""from django.contrib import admin"""
"""from utils.views import ResetPasswordRequestView, PasswordResetConfirmView"""
"""from django.conf.urls import include, url"""


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
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^recuperacao_senha(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #    PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    #url(r'^recuperacao_senha',
    #    ResetPasswordRequestView.as_view(), name="recuperacao_senha")"""

]
