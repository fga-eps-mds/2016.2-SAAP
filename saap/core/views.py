# coding=utf-8
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext
from core.models import Contato, Ticket
from autenticacao.models import OrganizadorContatos
from default.views import *

def capturar_campos(request):
    campos = [request.POST['nome'],request.POST['data_de_nascimento'],\
        request.POST['sexo'],request.POST['telefone'], request.POST['celular'],\
        request.POST['fax'], request.POST['cpf'], request.POST['rg'], request.POST['endereco'],\
        request.POST['cidade'], request.POST['cep'], request.POST['estado'], request.POST['email'],\
        request.POST['grupo'], request.POST['titulo'], request.POST['titulo_de_eleitor'], \
        request.POST['zona'],request.POST['secao'], request.POST['profissao'], \
        request.POST['cargo'], request.POST['empresa'],request.POST['dependente_nome'],\
        request.POST['dependente_aniversario'], request.POST['dependente_parentesco'],\
        request.POST['dependente_partido'],request.POST['dependente_data_filiacao']]
    return campos

class CadastroView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'cadastro_contato.html')
        return response

    def post (self,request):

        import ipdb
        ipdb.set_trace()

        campos = capturar_campos(request)

        if checar_vazio(campos) :

            nome = request.POST['nome']
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            telefone = request.POST['telefone']
            celular = request.POST['celular']
            fax = request.POST['fax']
            cpf = request.POST['cpf']
            rg= request.POST['rg']
            endereco = request.POST['endereco']
            cidade = request.POST['cidade']
            cep = request.POST['cep']
            estado = request.POST['estado']
            email = request.POST['email']
            grupo = request.POST['grupo']
            titulo = request.POST['titulo']
            titulo_de_eleitor = request.POST['titulo_de_eleitor']
            zona = request.POST['zona']
            secao = request.POST['secao']
            profissao = request.POST['profissao']
            cargo = request.POST['cargo']
            empresa = request.POST['empresa']
            dependente_nome = request.POST['dependente_nome']
            dependente_aniversario = request.POST['dependente_aniversario']
            dependente_parentesco = request.POST['dependente_parentesco']
            dependente_partido = request.POST['dependente_partido']
            dependente_data_filiacao = request.POST['dependente_data_filiacao']

            contato = Contato()
            contato.nome = nome
            contato.data_de_nascimento = data_de_nascimento
            contato.sexo = sexo
            contato.telefone = telefone
            contato.celular = celular
            contato.fax = fax
            contato.cpf = cpf
            contato.rg= rg
            contato.endereco = endereco
            contato.cidade = cidade
            contato.cep = cep
            contato.estado = estado
            contato.email = email
            contato.grupo = grupo
            contato.titulo = titulo
            contato.titulo_de_eleitor = titulo_de_eleitor
            contato.zona = zona
            contato.secao = secao
            contato.profissao = profissao
            contato.cargo = cargo
            contato.empresa = empresa
            contato.dependente_nome = dependente_nome
            contato.dependente_aniversario = dependente_aniversario
            contato.dependente_parentesco = dependente_parentesco
            contato.dependente_partido = dependente_partido
            contato.dependente_data_filiacao = dependente_data_filiacao
            contato.save()
            organizador = OrganizadorContatos.objects.get(username=request.user.username)
            organizador.contatos.add(contato)
            contatos = organizador.contatos.all()
            lista_contatos = list(contatos)
            response = render(request,'contato.html',locals())
        else:
            messages.error(request,'Preencha todos os campos!')
            organizador = OrganizadorContatos.objects.get(username=request.user.username)
            contatos = organizador.contatos.all()
            lista_contatos = list(contatos)
            response = render(request,'contato.html')

        return response

class DeletarContatoView(View):
    http_method_names = [u'get',u'post']

    def get (self, request):
        response = render(request, 'exclui_contato.html')
        return response

    def post(self, request):
        busca_email = request.POST['busca_email']

        if Contato.objects.get(email = busca_email).count() == 0:
            messages.error(request,'Contato nao existe!')
            response = render(request,'exclui_contato.html')
        else:
            c = Contato.objects.get(email = busca_email)
            c.delete()
            response = render(request,'cadastro_contato.html')

        return response

class AtualizaContato(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'atualiza_contato.html')
        return response

    def post(self, request):

        campos = capturar_campos(request)

        if checar_vazio(campos) :

            nome = request.POST['nome']
            data_de_nascimento = request.POST['data_de_nascimento']
            sexo = request.POST['sexo']
            telefone = request.POST['telefone']
            celular = request.POST['celular']
            fax = request.POST['fax']
            cpf = request.POST['cpf']
            rg= request.POST['rg']
            endereco = request.POST['endereco']
            cidade = request.POST['cidade']
            cep = request.POST['cep']
            estado = request.POST['estado']
            email = request.POST['email']
            grupo = request.POST['grupo']
            titulo = request.POST['titulo']
            titulo_de_eleitor = request.POST['titulo_de_eleitor']
            zona = request.POST['zona']
            secao = request.POST['secao']
            profissao = request.POST['profissao']
            cargo = request.POST['cargo']
            empresa = request.POST['empresa']
            dependente_nome = request.POST['dependente_nome']
            dependente_aniversario = request.POST['dependente_aniversario']
            dependente_parentesco = request.POST['dependente_parentesco']
            dependente_partido = request.POST['dependente_partido']
            dependente_data_filiacao = request.POST['dependente_data_filiacao']

            busca_email = request.POST['busca_email']
            organizador = OrganizadorContatos.objects.get(username=request.user.username)
            contato = organizador.contatos.get(email = busca_email)
            contato.nome = nome
            contato.data_de_nascimento = data_de_nascimento
            contato.sexo = sexo
            contato.telefone = telefone
            contato.celular = celular
            contato.fax = fax
            contato.cpf = cpf
            contato.rg= rg
            contato.endereco = endereco
            contato.cidade = cidade
            contato.cep = cep
            contato.estado = estado
            contato.email = email
            contato.grupo = grupo
            contato.titulo = titulo
            contato.titulo_de_eleitor = titulo_de_eleitor
            contato.zona = zona
            contato.secao = secao
            contato.profissao = profissao
            contato.cargo = cargo
            contato.empresa = empresa
            contato.dependente_nome = dependente_nome
            contato.dependente_aniversario = dependente_aniversario
            contato.dependente_parentesco = dependente_parentesco
            contato.dependente_partido = dependente_partido
            contato.dependente_data_filiacao = dependente_data_filiacao
            contato.save()
            contatos = organizador.contatos.all()
            lista_contatos = list(contatos)
            response = render(request,'contato.html',locals())
        else:
            messages.error(request,'Preencha todos os campos!')
            response = render(request,'atualiza_contato.html')

        return response


class ContatoView(View):
    http_method_names = [u'get', u'post']

    def get (self, request):
        return render_contatos_tickets(request)


class TicketView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            organizadores = OrganizadorContatos.objects.all()
            lista_organizadores = list(organizadores)
            response = render(request, 'ticket.html',locals())
        else:
            response = render(request, 'login.html')
        return response

    def post(self, request):

        novo_ticket = Ticket()

        # Checking if checkbox is checked
        if request.POST.get('enviar_anonimamente', False):
            anonimo = True
        else:
            anonimo = False

        titulo = request.POST['assunto']
        corpo_texto = request.POST.get('descricao')

        if anonimo is True:
            remetente = "Anonimo"
        else:
            remetente = request.user.get_full_name()

        tipo_ticket = request.POST['tipo_mensagem']
        arquivo_upload = None

        # Setting new ticket
        if request.user.is_authenticated() is False:

            response = render(request, 'login.html')
        else:
            novo_ticket.envio_anonimo = anonimo
            novo_ticket.titulo = titulo
            novo_ticket.corpo_texto = corpo_texto
            novo_ticket.remetente = remetente
            novo_ticket.gabinete_destino = None
            novo_ticket.tipo_ticket = tipo_ticket
            novo_ticket.file = arquivo_upload
            novo_ticket.save()
            organizador = OrganizadorContatos.objects.get(first_name=request.POST['nome_organizador'])
            organizador.tickets.add(novo_ticket)
            tickets = organizador.tickets.all()
            lista_tickets = list(tickets)

            response = render(request, 'perfil.html')

        return response

class PublicarTicketView(View):
    http_method_names = [u'get', u'post']

    def post(self, request):
        ticket_id = request.POST.get('ticket_id')
        ticket = Ticket.objects.get(id = ticket_id)
        ticket.aprovado = True

        if ticket.aprovado == True:
            ticket.save()
            messages.success(request, 'Ticket enviado para pagina do Vereador')
            organizadores = OrganizadorContatos.objects.all()
            lista_organizadores = list(organizadores)
            response = render (request, 'vereadores.html',locals()) #pagina do vereador
            return response

        else:
            messages.error(request, 'Erro ao tentar publicar Ticket')
            return render (request, 'redirect/')


class DeletarTicketView(View):
    http_method_names = [u'get']

    def get(self,request,pk):
        ticket = Ticket.objects.get(id=pk)
        ticket.delete()
        return redirect('/')


class VereadoresView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        organizadores = OrganizadorContatos.objects.all()
        lista_organizadores = list(organizadores)
        response = render(request, 'vereadores.html', locals())
        return response

    def post(self, request):

        campos_validados = checar_campos([request.POST['nome_organizador']])

        if campos_validados is True:

            organizador = OrganizadorContatos.objects.get(first_name=request.\
POST['nome_organizador'])
            tickets = organizador.tickets.filter(aprovado=True)
            lista_tickets = list(tickets)
            resposta = render(request, 'vereador.html', locals())

        else:
            organizadores = OrganizadorContatos.objects.all()
            lista_organizadores = list(organizadores)
            messages.error(request, 'É necessário selecionar algum vereador!')
            resposta = render(request, 'vereadores.html', locals())

        return resposta
