from django.shortcuts import render
from autenticacao.models import OrganizadorContatos

# Create your views here.

def checar_vazio(campos):
    nao_vazio = True
    for campo in campos:
        if campo == "":
            nao_vazio = False
    return nao_vazio

def render_contatos_tickets(request):
    organizador = OrganizadorContatos.objects.get(username=request.user.username)
    contatos = organizador.contatos.all()
    lista_contatos = list(contatos)
    tickets = organizador.tickets.all()
    lista_tickets = list(tickets)
    return render(request,'contato.html',locals())
