# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from autenticacao.models import OrganizadorContatos
from django.contrib import messages
from autenticacao.models import *
from core.models import *

from reportlab.pdfgen import canvas
from django.http import HttpResponse
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import StringIO
from django.core.files.storage import FileSystemStorage
from datetime import datetime

from django.core.mail import EmailMessage
from core.models import Grupo

# Create your views here.


campos_login = ["Nome de Usuário", "Senha"]
campos_cadastro = ["Gabinete", "Nome", "Sobrenome", "Nome de Usuário", "E-mail", \
    "Confirmar E-mail", "Senha", "Confirmar Senha", "Data de Nascimento", \
    "Sexo", "Município", "UF (Unidade Federativa)"]
campos_cadastro_cidadao = ["Nome", "Sobrenome", "Nome de Usuário", "E-mail", \
        "Confirmar E-mail", "Senha", "Confirmar Senha", "Data de Nascimento", \
        "Sexo", "Município", "UF (Unidade Federativa)"]
campos_ticket = ["Nome do Gabinete", "Tipo de Ticket", "Assunto", \
    "Mensagem"]
campos_mudar_senha = ["Nova Senha", "Confirmação Nova Senha"]
campos_excluir_conta = ["Senha"]
campos_cadastrar_contato = ["Nome", "Data de Nascimento", "Telefone \
    Residencial", "Sexo", "Telefone Celular", "CPF", "Fax", "RG", "Endereço",
    "Cidade", "Estado", "CEP", "E-mail", "Grupo", "Título", "Título de Eleitor",
    "Profissão", "Zona Eleitoral", "Cargo", "Seção Eleitoral", "Empresa", \
    "Nome do Dependente", "Aniversário do Dependente", "Parentesco do Dependente", \
    "Partido do Dependente", "Data de Filiação do Dependente", "E-mail do contato"]
campos_enviar_carta = ["Nome do remetente", "Município do remetente", \
    "Nome do destinatário", "Forma de tratamento", "Mensagem"]
campos_enviar_oficio = ["Nome do remetente", "Nome do destinatario", "Forma de tratamento", "Mensagem"]


def checar_administrador_gabinete(request, template, data):

    tipo_usuario = AdministradorGabinete.objects.filter(username=request.\
        user.username)
    if tipo_usuario.count():
        response = render(request, template, data)
    else:
        response = redirect('/')

    return response

def data_sexo():

    return {'campos_sexo': {'Masculino', 'Feminino'}}

def data_uf():

    return {'campos_uf': {'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', \
        'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', \
        'RN', 'RS', 'RO', 'RR', 'SC', 'SE', 'SP', 'TO'}}

def pegar_objeto_usuario(username):

    pegar_objeto = Cidadao.objects.filter(username=username)
    if pegar_objeto.count():
        return pegar_objeto[0]

    pegar_objeto = OrganizadorContatos.objects.filter(username=username)
    if pegar_objeto.count():
        return pegar_objeto[0]

    pegar_objeto = AdministradorGabinete.objects.filter(username=username)
    if pegar_objeto.count():
        return pegar_objeto[0]

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

    if template == "criar_administrador.html" or template == "criar_organizador.html":
        gabinetes = Gabinete.objects.all()
        lista_gabinetes = list(gabinetes)
        data['lista_gabinetes'] = lista_gabinetes
        response = render(request, template, data)
    else:
        response = render(request, template, data)

    return response

def checar_vazio(campos):
    nao_vazio = True
    for campo in campos:
        if campo == "":
            nao_vazio = False
    return nao_vazio

def render_contatos(request, resposta):
    gabinete = pegar_objeto_usuario(request.user.username).gabinete
    contatos = gabinete.contatos.all()
    lista_contatos = list(contatos)
    grupos = gabinete.grupos.all()
    lista_grupos = list(grupos)
    return render(request, 'contatos.html', locals())

def render_contatos_tickets(request):
    gabinete = pegar_objeto_usuario(request.user.username).gabinete
    contatos = gabinete.contatos.all()
    lista_contatos = list(contatos)
    tickets = gabinete.tickets.all()
    lista_tickets = list(tickets)
    lista_grupo = Grupo.objects.all()
    return render(request, "gabinete.html", locals())

def checar_campos_registro_cidadao(request):

    campos_validados = checar_campos([request.POST['first_name'], \
        request.POST['last_name'], request.POST['username'], \
        request.POST['email'], request.POST['confirmacao_email'], \
        request.POST['password'], request.POST['confirmacao_password'], \
        request.POST['data_de_nascimento'], request.POST['sexo'], \
        request.POST['municipio'], request.POST['uf']])

    return campos_validados

def checar_campos_registro_admin(request):

    campos_validados = checar_campos([request.POST['nome_gabinete'],
        request.POST['first_name'], request.POST['last_name'],
        request.POST['username'], request.POST['email'],
        request.POST['confirmacao_email'], request.POST['password'],
        request.POST['confirmacao_password'], request.POST['data_de_nascimento'],
        request.POST['sexo'], request.POST['municipio'],
        request.POST['uf']])

    return campos_validados

def checar_existe_usuario(username):

    if Cidadao.get_usuario_por_username(username).count() == 0 and \
        OrganizadorContatos.get_usuario_por_username(username).count() == 0:
        return True
    else:
        return False

def atualizar_contato(request, contato):

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
    contato.grupo_contato = grupo
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

    return contato

def checar_validacoes_usuario(request, template, campos, data):

    try:
        gabinete = pegar_objeto_usuario(request.user.username).gabinete
    except:
        pass

    if campos[0] == "Gabinete":
        campos_validados = checar_campos_registro_admin(request)
    else:
        campos_validados = checar_campos_registro_cidadao(request)

    if campos_validados is True:
        pass
        if checar_data(request.POST['data_de_nascimento']):
            pass
            if checar_existe_usuario(request.POST['username']):
                return True
            else:
                response = render_mensagem_erro(request, 'Já existe um \
                    usuário com esse "Nome de Usuário"!', \
                    template, locals())
        else:
            response = render_mensagem_erro(request, 'Formato de data \
                inválido (AAAA-MM-DD)!', template, locals())
    else:
        response = render_mensagem_erro(request, 'O campo "%s" não foi \
            preenchido!' % campos[campos_validados], \
            template, locals())

    return response

def gerar_pdf_carta(carta):

    doc = SimpleDocTemplate("/tmp/carta.pdf")
    styles = getSampleStyleSheet()

    mensagem = carta.texto
    mensagem = mensagem.replace('\n', '<br/>')

    Story=[]

    now = datetime.now()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<font size=12>%s, %s/%s/%s</font>' % (carta.municipio_remetente, now.day, now.month, now.year)
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 24))

    ptext = '<font size=12>%s %s,</font>' % (carta.forma_tratamento, carta.nome_destinatario)
    Story.append(Paragraph(ptext, styles["Normal"]))
    #.split()[0].strip()

    Story.append(Spacer(1, 36))

    ptext = '<font size=12>Prezado %s:</font>' % carta.forma_tratamento
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    ptext = '<font size=12>%s</font>' % mensagem
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 36))

    ptext = '<font size=12>Atenciosamente,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    ptext = '<font size=12>%s</font>' % carta.nome_remetente
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    doc.build(Story)

    fs = FileSystemStorage("/tmp")
    with fs.open("carta.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="carta.pdf"'
    return response

def gerar_pdf_oficio(oficio):

    doc = SimpleDocTemplate("/tmp/oficio.pdf")
    styles = getSampleStyleSheet()

    corpo_texto_doc = oficio.corpo_texto_doc
    corpo_texto_doc = corpo_texto_doc.replace('\n', '<br/>')

    Story=[]

    now = datetime.now()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story.append(Spacer(1, 24))

    ptext = '<font size=12>Oficio nº __ , %s </font>' % (now.year)
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 24))

    ptext = '<font size=12>À Gabinete </font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    ptext = '<font size=12>Prezado %s %s, %s</font>' % (oficio.forma_tratamento, oficio.destinatario,oficio.corpo_texto_doc)
    Story.append(Paragraph(ptext, styles["Justify"]))

    Story.append(Spacer(1, 36))

    ptext = '<font size=12>Atenciosamente,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    ptext = '<font size=12>%s, %s/%s/%s</font>' % (oficio.remetente, now.day, now.month, now.year)
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))

    doc.build(Story)

    fs = FileSystemStorage("/tmp")
    with fs.open("oficio.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="oficio.pdf"'
        return response


def enviar_carta_email(request, carta):

    email = EmailMessage('Carta de ' + carta.nome_remetente,
        '%s, %s/%s/%s\n\n%s %s,\n\n\nPrezado %s:\n\n%s\n\n\nAtenciosamente,\
            \n\n%s' % (carta.municipio_remetente, carta.data.day, \
            carta.data.month, carta.data.year, carta.forma_tratamento, \
            carta.nome_destinatario, carta.forma_tratamento, carta.texto, \
            carta.nome_remetente),
        to=[request.POST['email_carta']])
    email.send()

    return redirect('/gabinete/cartas/', messages.success(request, 'Carta enviada por e-mail com sucesso!'))

def enviar_oficio_email(request, oficio):
    email = EmailMessage('Oficio de ' + oficio.remetente,
           'Hoje, dia %s/%s/%s\n\n\nPrezado %s %s:\n\n%s\n\n\nAtenciosamente,\
            \n\n%s' % (oficio.data.day,oficio.data.month,oficio.data.year,\
            oficio.forma_tratamento, oficio.destinatario, \
            oficio.corpo_texto_doc, oficio.remetente),
        to=[request.POST['email_oficio']])
    email.send()

    return redirect('/gabinete/oficios/', messages.success(request, 'Oficio enviado por e-mail com sucesso!'))

def carregar_pagina_carta_oficio(request, endereco):
    try:
        gabinete = pegar_objeto_usuario(request.user.username).gabinete
        cartas = gabinete.cartas.all()
        lista_cartas = list(cartas)
        oficios = gabinete.oficios.all()
        lista_oficios = list(oficios)
    except:
        pass
    response = checar_administrador_gabinete(request, endereco, locals())
    return response

def deletar_objeto(Objeto, endereco, pk):
    objeto = Objeto.objects.get(id=pk)
    objeto.delete()
    return redirect(endereco)

def get_padrao_cadastro_gerar(request, endereco):
    gabinete = pegar_objeto_usuario(request.user.username).gabinete
    response = render(request, endereco, locals())
    return response

def checar_busca(busca, query, Q):
    if busca == 'cidade':
        resposta = Contato.objects.filter(cidade__startswith=query)
    elif busca == 'genero':
        resposta = Contato.objects.filter(sexo__contains=query)
    elif busca == 'estado':
        resposta = Contato.objects.filter(estado__startswith=query)
    else:
        return checar_busca_continuacao(busca, query, Q)
    return resposta

def checar_busca_continuacao(busca, query, Q):
    if busca == 'data_aniversario':
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
    return resposta

def enviar_carta_oficio_email(request, Objeto, pk):

    if Objeto.objects.get(id=pk).__class__.__name__ == 'Oficio':
        return enviar_oficio_email(request, Objeto.objects.get(id=pk))
    else:
        return enviar_carta_email(request, Objeto.objects.get(id=pk))
