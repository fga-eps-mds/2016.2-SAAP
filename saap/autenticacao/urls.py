# coding=utf-8
from django.conf.urls import url
from .views import (LoginView, RegistroView)
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
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^recuperacao_senha(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #    PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    #url(r'^recuperacao_senha',
    #    ResetPasswordRequestView.as_view(), name="recuperacao_senha")"""

]
