# coding=utf-8
from django.conf.urls import url
from .views import (CadastroView, DeletarContatoView, ContatoView)

urlpatterns = [
    url(r'^cadastro_contato/$', CadastroView.as_view(),
        name='cadastro_contato'),
    url(r'^exclui_contato/$', DeletarContatoView.as_view(),
        name='exclui_contato'),
    url(r'^contato/$', ContatoView.as_view(),
        name='contato'),

]
