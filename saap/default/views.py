from django.shortcuts import render
from autenticacao.models import OrganizadorContatos
from django.contrib import messages

# Create your views here.

def checar_campos(campos):
    for i in range(len(campos)):
        if campos[i] == "":
            return i
    return True

def render_mensagem_erro(request, mensagem, template, data):
    messages.error(request, mensagem)
    response = render(request, template, data)
    return response

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
