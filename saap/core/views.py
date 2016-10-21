# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext
from core.models import Contato, Ticket
from default.views import *
from autenticacao.views import *
from autenticacao.models import *
from django.views.generic.list import ListView
from django.db.models import Q
from core.models import Grupo


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

                        gabinete = pegar_objeto_usuario(request.user.username).gabinete

                        contato = Contato()
                        contato = atualizar_contato(request, contato)
                        gabinete.contatos.add(contato)

                        response = render_contatos_tickets(request)

                    else:
                        return render_mensagem_erro(request, 'Formato de data \
                            inválido (AAAA-MM-DD) no campo Data de Filiação do \
                            Dependente!', 'cadastro_contato.html', {'data':data})
                else:
                    return render_mensagem_erro(request, 'Formato de data \
                        inválido (AAAA-MM-DD) no campo Aniversário do \
                        Dependente!', 'cadastro_contato.html', {'data':data})
            else:
                return render_mensagem_erro(request, 'Formato de data \
                    inválido (AAAA-MM-DD) no campo Data de Nascimento!',\
                    'cadastro_contato.html', {'data':data})
        else:
            response = render_mensagem_erro(request, 'O campo %s não foi \
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

        if Contato.objects.filter(email = busca_email).count() == 0:
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

            gabinete = pegar_objeto_usuario(request.user.username).gabinete

            busca_email = request.POST['busca_email']
            contato = gabinete.contatos.get(email = busca_email)
            contato = atualizar_contato(request, contato)

            response = render_contatos_tickets(request)
        else:
            response = render_mensagem_erro(request, 'O campo %s não foi \
                preenchido!' % campos_cadastrar_contato[campos_validados], \
                'atualiza_contato.html', {'data':data})

        return response

class ContatoView(View):
    http_method_names = [u'get', u'post']

    def get (self, request):
        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        contatos = gabinete.contatos.all()
        lista_contatos = list(contatos)
        return render(request, 'contatos.html', locals())

class TicketsView(View):
    http_method_names = [u'get', u'post']

    def get (self, request):
        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        tickets = gabinete.tickets.all()
        lista_tickets = list(tickets)

        response = checar_administrador_gabinete(request, 'tickets.html', locals())

        return response

class GabineteView(View):
    http_method_names = [u'get', u'post']

    def get (self, request):

        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        contatos = gabinete.contatos.all()
        lista_contatos = list(contatos)
        tickets = gabinete.tickets.all()
        lista_tickets = list(tickets)

        response = checar_administrador_gabinete(request, 'gabinete.html', locals())

        return response

class TicketView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        if request.user.is_authenticated():
            gabinetes = Gabinete.objects.all()
            lista_gabinetes = list(gabinetes)
            response = render(request, 'ticket.html',locals())
        else:
            response = render(request, 'login.html')
        return response

    def post(self, request):

        data = {}
        data['campos_tipo_mensagem'] = ['Incidente', 'Requisição', 'Melhorias']
        data['nome_gabinete'] = request.POST['nome_gabinete']
        data['tipo_mensagem'] = request.POST['tipo_mensagem']
        data['assunto'] = request.POST['assunto']
        data['descricao'] = request.POST['descricao']

        campos_validados = checar_campos([request.POST['nome_gabinete'], \
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
                gabinete = Gabinete.objects.get(nome_gabinete = \
                    request.POST['nome_gabinete'])
                gabinete.tickets.add(novo_ticket)
                tickets = gabinete.tickets.all()
                lista_tickets = list(tickets)

                response = render(request, 'perfil.html')

        else:
            messages.error(request, 'O campo %s não foi preenchido!' \
                % campos_ticket[campos_validados])
            gabinetes = Gabinete.objects.all()
            lista_gabinetes = list(gabinetes)
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
            gabinetes = Gabinete.objects.all()
            lista_gabinetes = list(gabinetes)
            response = render (request, 'gabinetes.html',locals()) #pagina do vereador
            return response

        # else:
        #     messages.error(request, 'Erro ao tentar publicar Ticket')
        #     return render (request, 'redirect/')


class DeletarTicketView(View):
    http_method_names = [u'get']

    def get(self,request,pk):
        ticket = Ticket.objects.get(id=pk)
        ticket.delete()
        return redirect('/')


class GabinetesView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        gabinetes = Gabinete.objects.all()
        lista_gabinetes = list(gabinetes)
        response = render(request, 'gabinetes.html', locals())
        return response

    def post(self, request):

        campos_validados = checar_campos([request.POST['nome_gabinete']])

        if campos_validados is True:

            gabinete = Gabinete.objects.get(nome_gabinete = request.\
POST['nome_gabinete'])
            tickets = gabinete.tickets.filter(aprovado=True)
            lista_tickets = list(tickets)
            resposta = render(request, 'visualizar_gabinete.html', locals())

        else:
            gabinetes = Gabinete.objects.all()
            lista_gabinetes = list(gabinetes)
            messages.error(request, 'É necessário selecionar algum gabinete!')
            resposta = render(request, 'gabinetes.html', locals())

        return resposta


class GerarCartaView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):

        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        response = checar_administrador_gabinete(request, 'gerar_carta.html', locals())

        return response

    def post(self, request):

        data = {}
        data['nome_remetente'] = request.POST['nome_remetente']
        data['municipio_remetente'] = request.POST['municipio_remetente']
        data['nome_destinatario'] = request.POST['nome_destinatario']
        data['forma_tratamento'] = request.POST['forma_tratamento']
        data['mensagem'] = request.POST['mensagem']
        data['campos_forma_tratamento'] = ['Senhor(a)', 'Doutor(a)']

        campos_validados = checar_campos([request.POST['nome_remetente'], \
            request.POST['municipio_remetente'], request.POST\
            ['nome_destinatario'], request.POST['forma_tratamento'], \
            request.POST['mensagem']])

        if campos_validados is True:

            carta = Carta()
            carta.nome_remetente = request.POST['nome_remetente']
            carta.municipio_remetente = request.POST['municipio_remetente']
            carta.nome_destinatario = request.POST['nome_destinatario']
            carta.forma_tratamento = request.POST['forma_tratamento']
            carta.texto = request.POST['mensagem']
            carta.data = datetime.now()
            carta.save()
            gabinete = pegar_objeto_usuario(request.user.username).gabinete
            gabinete.cartas.add(carta)
            response = redirect('/gabinete/cartas/')

        else:
            messages.error(request, 'O campo "%s" não foi preenchido!' \
                % campos_enviar_carta[campos_validados])
            response = render(request, 'gerar_carta.html', locals())

        return response

class CartasView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):
        try:
            gabinete = pegar_objeto_usuario(request.user.username).gabinete
            cartas = gabinete.cartas.all()
            lista_cartas = list(cartas)
        except:
            pass
        response = checar_administrador_gabinete(request, 'cartas.html', locals())

        return response

class DeletarCartaView(View):
    http_method_names = [u'get']

    def get(self,request,pk):
        carta = Carta.objects.get(id=pk)
        carta.delete()
        return redirect('/cartas/')

class GerarPDFCartaView(View):
    http_method_names = [u'get']

    def get(self, request, pk):
        carta = Carta.objects.get(id=pk)
        return gerar_pdf_carta(carta)

class EnviarCartaView(View):
    http_method_names = [u'post']

    def post(self, request, pk):
        carta = Carta.objects.get(id=pk)
        return enviar_carta_email(request, carta)


class BuscaContatosView(ListView):
    http_method_names = [u'post']

    model = Contato 

    template_name = 'contato.html'

    def post(self, request):
        busca = str(request.POST['tipo_busca']).lower()
        query = request.POST['pesquisa']

        if busca == 'cidade':
            resposta = Contato.objects.filter(cidade__startswith=query)
        elif busca == 'genero':
            resposta = Contato.objects.filter(sexo__contains=query)
        elif busca == 'estado':
            resposta = Contato.objects.filter(estado__startswith=query)
        elif busca == 'data_aniversario':
            resposta = Contato.objects.filter(data_de_nascimento__month=query)
        elif busca == 'nome':
            resposta = Contato.objects.filter(nome__contains=query)
        else:
            resposta = Contato.objects.filter(
            Q(nome__contains=query) |
            Q(sexo = query) |
            Q(estado__contains=query) |
            Q(cidade__contains=query) |
            Q(data_de_nascimento__contains=query)
            )

        # resposta = list(resposta)

        return render(request, 'contato.html', locals())

class CriarGrupoDeContatosView(View):

    http_method_names = [u'get', u'post']

    def post(self,request):

        nome_grupo = request.POST['nome_grupo']
        novo_grupo = Grupo()
        novo_grupo.nome = nome_grupo
        novo_grupo.save()

        return redirect("/")

class AdicionarContatoAoGrupo(View):

    http_method_names = [u'post']

    def post(self,request):

        contatos = request.POST.getlist('contatos')

        nome_grupo = request.POST['nome_grupo']

        s_grupo = Grupo.objects.filter(nome__contains=nome_grupo)

        grupo = s_grupo[0]

        for contato in contatos:
            grupo.contatos.add(contato)

        return redirect('/')

class GrupoDeContatos(ListView):
    http_method_names = [u'get', u'post']


class GrupoDeContatosView(ListView):

    http_method_names = [u'get', u'post']

    model = Contato #grupo
    template_name = 'contato.html'

    def getGrupo (self, **kwargs):
        return Contato.objects(grupo)

    def getData (self, **kwargs):
        return Contato.objects.filter(data_de_nascimento)

    def getBairro (self, **kwargs):
        return Contato.objects.filter(bairro)

    def getCidade(self, **kwargs):
        return Contato.objects.filter(cidade)

    def getCEP(self, **kwargs):
        return Contato.objects.filter(CEP)

    def getUF (self, **kwargs):
        return Contato.objects.filter(UF)

    def post(self, request):
        busca = str(request.POST['tipo_busca']).lower()
        query = request.POST['pesquisa']

        if busca == 'cidade':
            resposta = Contato.objects.filter(cidade__startswith=query)
        elif busca == 'genero':
            resposta = Contato.objects.filter(sexo__contains=query)
        elif busca == 'estado':
            resposta = Contato.objects.filter(estado__startswith=query)
        elif busca == 'data_aniversario':
            resposta = Contato.objects.filter(data_de_nascimento__month=query)
        elif busca == 'nome':
            resposta = Contato.objects.filter(nome__contains=query)
        else:
            resposta = Contato.objects.filter(
            Q(nome__contains=query) |
            Q(sexo = query) |
            Q(estado__contains=query) |
            Q(cidade__contains=query) |
            Q(data_de_nascimento__contains=query)
            )

        # resposta = list(resposta)

        return render(request, 'contato.html', locals())

class CriarGrupoDeContatosView(View):

    http_method_names = [u'get', u'post']

    def post(self,request):

        nome_grupo = request.POST['nome_grupo']
        novo_grupo = Grupo()
        novo_grupo.nome = nome_grupo
        novo_grupo.save()

        return redirect("/")

class AdicionarContatoAoGrupo(View):

    http_method_names = [u'post']

    def post(self,request):

        contatos = request.POST.getlist('contatos')

        nome_grupo = request.POST['nome_grupo']

        s_grupo = Grupo.objects.filter(nome__contains=nome_grupo)

        grupo = s_grupo[0]

        for contato in contatos:
            grupo.contatos.add(contato)

        return redirect('/')

class GerarOficioView(View):
    http_method_names = [u'get', u'post']

    def get(self, request):

        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        response = checar_administrador_gabinete(request, 'gerar_oficio.html', locals())

        return response

    def post(self, request):

        data = {}
        data['remetente'] = request.POST['remetente']
        data['forma_tratamento'] = request.POST['forma_tratamento']
        data['destinatario'] = request.POST['destinatario']
        data['corpo_texto_doc'] = request.POST['corpo_texto_doc']
        data['campos_forma_tratamento'] = ['Senhor(a)', 'Doutor(a)']

        campos_validados = checar_campos([request.POST['remetente'], \
            request.POST['forma_tratamento'], request.POST['destinatario'], \
            request.POST['corpo_texto_doc']])

        if campos_validados is True:

            oficio = Oficio()
            oficio.remetente = request.POST['remetente']
            oficio.destinatario = request.POST['destinatario']
            oficio.corpo_texto_doc = request.POST['corpo_texto_doc']
            oficio.forma_tratamento = request.POST['forma_tratamento']
            oficio.data = datetime.now()
            oficio.save()

            gabinete = pegar_objeto_usuario(request.user.username).gabinete
            gabinete.oficios.add(oficio)
            response = redirect("/gabinete/oficios/")

        else:
            messages.error(request, 'O campo "%s" não foi preenchido!'\
            % campos_enviar_oficio[campos_validados])

            response = render(request, 'gerar_oficio.html', locals())

        return response


class OficioView(View):
     http_method_names = [u'get', u'post']

     def get(self, request):
        try:
            gabinete = pegar_objeto_usuario(request.user.username).gabinete
            oficios = gabinete.oficios.all()
            lista_oficios = list(oficios)
        except:
            pass
        response = checar_administrador_gabinete(request, 'oficios.html', locals())

        return response


class DeletarOficioView(View):
    http_method_names = [u'get']

    def get(self,request,pk):
        oficio = Oficio.objects.get(id=pk)
        oficio.delete()
        return redirect('/oficio/')

class GerarPDFOficioView(View):
    http_method_names = [u'get']

    def get(self, request, pk):
        oficio = Oficio.objects.get(id=pk)
        return gerar_pdf_oficio(oficio)

class EnviarOficioView(View):
    http_method_names = [u'post']

    def post(self, request, pk):
        oficio = Oficio.objects.get(id=pk)
        return enviar_oficio_email(request, oficio)


class GrupoDeContatos(ListView):
    http_method_names = [u'get', u'post']



class BuscaContatosView(ListView):
    http_method_names = [u'post']

    model = Contato 
    template_name = 'contato.html'


    def getGrupo (self, **kwargs):
        return Contato.objects(grupo)

    def getData (self, **kwargs):
        return Contato.objects.filter(data_de_nascimento)

    def getBairro (self, **kwargs):
        return Contato.objects.filter(bairro)

    def getCidade(self, **kwargs):
        return Contato.objects.filter(cidade)

    def getCEP(self, **kwargs):
        return Contato.objects.filter(CEP)

    def getUF (self, **kwargs):
        return Contato.objects.filter(UF)

    def post(self, request):
        busca = str(request.POST['tipo_busca']).lower()
        query = request.POST['pesquisa']

        if busca == 'cidade':
            resposta = Contato.objects.filter(cidade__startswith=query)
        elif busca == 'genero':
            resposta = Contato.objects.filter(sexo__contains=query)
        elif busca == 'estado':
            resposta = Contato.objects.filter(estado__startswith=query)
        elif busca == 'data_aniversario':
            resposta = Contato.objects.filter(data_de_nascimento__month=query)
        elif busca == 'nome':
            resposta = Contato.objects.filter(nome__contains=query)
        else:
            resposta = Contato.objects.filter(
            Q(nome__contains=query) |
            Q(sexo = query) |
            Q(estado__contains=query) |
            Q(cidade__contains=query) |
            Q(data_de_nascimento__contains=query)
            )

        # resposta = list(resposta)

        return render(request, 'contato.html', locals())

class CriarGrupoDeContatosView(View):

    http_method_names = [u'get', u'post']

    def post(self,request):

        nome_grupo = request.POST['nome_grupo']
        novo_grupo = Grupo()
        novo_grupo.nome = nome_grupo
        novo_grupo.save()

        return render(request,'contato.html')


class AdicionarContatoAoGrupo(View):

    http_method_names = [u'post']

    def post(self,request):

        contatos = request.POST.getlist('contatos')

        nome_grupo = request.POST['nome_grupo']

        s_grupo = Grupo.objects.filter(nome__contains=nome_grupo)

        grupo = s_grupo[0]

        for contato in contatos:
            grupo.contatos.add(contato)

        return redirect('/')

class GrupoDeContatos(ListView):
    http_method_names = [u'get', u'post']

