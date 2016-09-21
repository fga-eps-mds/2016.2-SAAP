# coding=utf-8
from django.conf.urls import url
from .views import (CadastroView, DeletarContatoView, ContatoView, TicketView, AtualizaContato)


urlpatterns = [
    url(r'^cadastro_contato/$', CadastroView.as_view(),
        name='cadastro_contato'),
    url(r'^exclui_contato/$', DeletarContatoView.as_view(),
        name='exclui_contato'),
    url(r'^contato/$', ContatoView.as_view(),
        name='contato'),
    url(r'^atualiza_contato/$', AtualizaContato.as_view(),
        name='atualiza_contato'),
    url(r'^ticket/$', TicketView.as_view(),
        name='ticket'),


]
