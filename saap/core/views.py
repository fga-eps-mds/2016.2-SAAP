# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext
from core.models import Contato, Ticket
from autenticacao.models import OrganizadorContatos
from default.views import *

class CadastroView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        response = render(request, 'cadastro_contato.html')
        return response

    def post (self,request):

        data = {}
        data['campos_sexo'] = ['Masculino', 'Feminino']
        data['campos_grupos'] = ['Grupo 1', 'Grupo 2', 'Grupo 3']
        data['campos_titulos'] = ['Senhor', 'Doutor']
        data['nome'] = request.POST['nome']
        data['data_de_nascimento'] = request.POST['data_de_nascimento']
        data['telefone'] = request.POST['telefone']
        data['sexo'] = request.POST['sexo']
        data['celular'] = request.POST['celular']
        data['cpf'] = request.POST['cpf']
        data['fax'] = request.POST['fax']
        data['rg'] = request.POST['rg']
        data['endereco'] = request.POST['endereco']
        data['cidade'] = request.POST['cidade']
        data['estado'] = request.POST['estado']
        data['cep'] = request.POST['cep']
        data['email'] = request.POST['email']
        data['grupo'] = request.POST['grupo']
        data['titulo'] = request.POST['titulo']
        data['titulo_de_eleitor'] = request.POST['titulo_de_eleitor']
        data['profissao'] = request.POST['profissao']
        data['zona'] = request.POST['zona']
        data['cargo'] = request.POST['cargo']
        data['secao'] = request.POST['secao']
        data['empresa'] = request.POST['empresa']
        data['dependente_nome'] = request.POST['dependente_nome']
        data['dependente_aniversario'] = request.POST['dependente_aniversario']
        data['dependente_parentesco'] = request.POST['dependente_parentesco']
        data['dependente_partido'] = request.POST['dependente_partido']
        data['dependente_data_filiacao'] = request.POST['dependente_data_\
filiacao']

        campos_validados = checar_campos([request.POST['nome'], \
            request.POST['data_de_nascimento'], request.POST['telefone'], \
            request.POST['sexo'], request.POST['celular'], request.POST['cpf'],\
            request.POST['fax'], request.POST['rg'], request.POST['endereco'], \
            request.POST['cidade'], request.POST['estado'], \
            request.POST['cep'], request.POST['email'], request.POST['grupo'], \
            request.POST['titulo'], request.POST['titulo_de_eleitor'], \
            request.POST['profissao'], request.POST['zona'], request.POST['cargo'], \
            request.POST['secao'], request.POST['empresa'], \
            request.POST['dependente_nome'], request.POST['dependente_aniversario'], \
            request.POST['dependente_parentesco'], request.POST['dependente_partido'],\
            request.POST['dependente_data_filiacao']])

        if campos_validados is True:

            if checar_data(request.POST['data_de_nascimento']):

                if checar_data(request.POST['dependente_aniversario']):

                    if checar_data(request.POST['dependente_data_filiacao']):

                        organizador = OrganizadorContatos.objects.get(\
                            username=request.user.username)

                        contato = Contato()
                        contato = atualizar_contato(request, contato)
                        organizador.contatos.add(contato)

                        response = render_contatos_tickets(request)

                    else:
                        return render_mensagem_erro(request, 'Formato de data \
                            inválido (AAAA-MM-DD) no campo "Data de Filiação do \
                            Dependente"!', 'cadastro_contato.html', {'data':data})
                else:
                    return render_mensagem_erro(request, 'Formato de data \
                        inválido (AAAA-MM-DD) no campo "Aniversário do \
                        Dependente"!', 'cadastro_contato.html', {'data':data})
            else:
                return render_mensagem_erro(request, 'Formato de data \
                    inválido (AAAA-MM-DD) no campo "Data de Nascimento"!',\
                    'cadastro_contato.html', {'data':data})
        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_cadastrar_contato[campos_validados], \
                'cadastro_contato.html', {'data':data})

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

        campos_validados = checar_campos([request.POST['nome'], \
            request.POST['data_de_nascimento'], request.POST['telefone'], \
            request.POST['sexo'], request.POST['celular'], request.POST['cpf'],\
            request.POST['fax'], request.POST['rg'], request.POST['endereco'], \
            request.POST['cidade'], request.POST['estado'], \
            request.POST['cep'], request.POST['email'], request.POST['grupo'], \
            request.POST['titulo'], request.POST['titulo_de_eleitor'], \
            request.POST['profissao'], request.POST['zona'], request.POST['cargo'], \
            request.POST['secao'], request.POST['empresa'], \
            request.POST['dependente_nome'], request.POST['dependente_aniversario'], \
            request.POST['dependente_parentesco'], request.POST['dependente_partido'],\
            request.POST['dependente_data_filiacao'], request.POST['busca_email']])

        if campos_validados is True:

            organizador = OrganizadorContatos.objects.get(username=request.user.username)

            busca_email = request.POST['busca_email']
            contato = organizador.contatos.get(email = busca_email)
            contato = atualizar_contato(request, contato)

            response = render_contatos_tickets(request)
        else:
            response = render_mensagem_erro(request, 'O campo "%s" não foi \
                preenchido!' % campos_cadastrar_contato[campos_validados], \
                'atualiza_contato.html', {'data':data})

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

        data = {}
        data['campos_tipo_mensagem'] = ['Incidente', 'Requisição', 'Melhorias']
        data['nome_organizador'] = request.POST['nome_organizador']
        data['tipo_mensagem'] = request.POST['tipo_mensagem']
        data['assunto'] = request.POST['assunto']
        data['descricao'] = request.POST['descricao']

        campos_validados = checar_campos([request.POST['nome_organizador'], \
            request.POST['tipo_mensagem'], request.POST['assunto'], \
            request.POST['descricao']])

        if campos_validados is True:

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
                organizador = OrganizadorContatos.objects.get(first_name = \
                    request.POST['nome_organizador'])
                organizador.tickets.add(novo_ticket)
                tickets = organizador.tickets.all()
                lista_tickets = list(tickets)

                response = render(request, 'perfil.html')

        else:
            messages.error(request, 'O campo "%s" não foi preenchido!' \
                % campos_ticket[campos_validados])
            organizadores = OrganizadorContatos.objects.all()
            lista_organizadores = list(organizadores)
            response = render(request, 'ticket.html', locals())

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
