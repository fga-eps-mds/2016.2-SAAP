# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (CadastroView, DeletarContatoView, ContatoView, TicketView, 
                    AtualizaContato, VereadoresView, PublicarTicketView, 
                    DeletarTicketView)

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
    url(r'^publicar_ticket/$', PublicarTicketView.as_view(),
        name='publicar_ticket'),
    url(r'^deletar_ticket/(?P<pk>[0-9]+)/$', DeletarTicketView.as_view(),
        name='deletar_ticket'),
    url(r'^vereadores/$', VereadoresView.as_view(),
        name='vereadores'),
]
