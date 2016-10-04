from django.shortcuts import render
from autenticacao.models import OrganizadorContatos
from django.contrib import messages

# Create your views here.

campos_login = ["Nome de Usuário", "Senha"]
campos_cadastro = ["Nome", "Sobrenome", "Nome de Usuário", "E-mail", \
    "Confirmar E-mail", "Senha", "Confirmar Senha", "Data de Nascimento", \
    "Sexo", "Município", "UF (Unidade Federativa)"]

def checar_data(data):
    partes_data = data.split("-")

    if len(partes_data) == 3:
        if [len(partes_data[0]), len(partes_data[1]), len(partes_data[2])] == \
            [4, 2, 2]:
            return True
    return False

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
