from django.shortcuts import render
from autenticacao.models import OrganizadorContatos
from django.contrib import messages
from autenticacao.models import *

# Create your views here.

data = {}
data['campos_sexo'] = ['Masculino', 'Feminino']
data['campos_uf'] = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', \
    'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', \
    'RN', 'RS', 'RO', 'RR', 'SC', 'SE', 'SP', 'TO']
campos_login = ["Nome de Usuário", "Senha"]
campos_cadastro = ["Nome", "Sobrenome", "Nome de Usuário", "E-mail", \
    "Confirmar E-mail", "Senha", "Confirmar Senha", "Data de Nascimento", \
    "Sexo", "Município", "UF (Unidade Federativa)"]
campos_ticket = ["Nome do Organizador", "Tipo de Ticket", "Assunto", \
    "Mensagem"]
campos_mudar_senha = ["Nova Senha", "Confirmação Nova Senha"]
campos_excluir_conta = ["Senha"]
campos_cadastrar_contato = ["Nome", "Data de Nascimento", "Telefone \
    Residencial", "Sexo", "Telefone Celular", "CPF", "Fax", "RG", "Endereço",
    "Cidade", "Estado", "CEP", "E-mail", "Grupo", "Título", "Título de Eleitor",
    "Profissão", "Zona Eleitoral", "Cargo", "Seção Eleitoral", "Empresa", \
    "Nome do Dependente", "Aniversário do Dependente", "Parentesco do Dependente", \
    "Partido do Dependente", "Data de Filiação do Dependente", "E-mail do contato"]

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

def checar_campos_registro(request):

    campos_validados = checar_campos([request.POST['first_name'], \
        request.POST['last_name'], request.POST['username'], \
        request.POST['email'], request.POST['confirmacao_email'], \
        request.POST['password'], request.POST['confirmacao_password'], \
        request.POST['data_de_nascimento'], request.POST['sexo'], \
        request.POST['municipio'], request.POST['uf']])

    return campos_validados

def checar_existe_usuario(username):

    if Cidadao.get_usuario_por_username(username).count() == 0 and \
        OrganizadorContatos.get_usuario_por_username(username).count() == 0:
        return True
    else:
        return False
