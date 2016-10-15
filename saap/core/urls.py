# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (CadastroView, DeletarContatoView, ContatoView, TicketView, AtualizaContato)


urlpatterns = [
    url(r'^cadastro_contato/$', login_required(CadastroView.as_view()),
        name='cadastro_contato'),
    url(r'^exclui_contato/$', login_required(DeletarContatoView.as_view()),
        name='exclui_contato'),
    url(r'^contato/$', login_required(ContatoView.as_view()),
        name='contato'),
    url(r'^atualiza_contato/$', login_required(AtualizaContato.as_view()),
        name='atualiza_contato'),
    url(r'^ticket/$', TicketView.as_view(),
        name='ticket'),
]
