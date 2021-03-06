from django.shortcuts import render,redirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from controleacesso.models import Pessoa
from controleacesso.models import Acesso
from controleacesso.logic import threadProcessarFace
from rest_framework import serializers
import datetime
from datetime import timedelta
from PIL import Image
from django.contrib.auth import password_validation
import csv
from django.http import HttpResponse
from threading import Thread
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
# Create your views here.

@csrf_protect
def login(request):
	data = {}
	if request.method == 'POST':
		data['username'] = request.POST.get("usuario")
		data['password'] = request.POST.get("senha")
		user = authenticate(username=data['username'], password=data['password'])
		if user is not None:
			auth_login(request,user)
			return HttpResponseRedirect('/cadastrar')
		messages.error(request, "Usuário ou senha invalido!")
	return render(request, 'formulario/login.html')

@login_required(login_url='/')
def cad_face(request):
	data = {}
	if request.method == 'POST':
		if 'img' in request.FILES:
			uploaded_file = request.FILES['img']
			data['nome'] = request.POST.get("name")
			data['codigo'] = request.POST.get("code")
			data['check'] = bool(request.POST.get("scales"))
			if data['nome'] != "" and data['check'] == True:
				pes = Pessoa.objects.create_Pessoa(data['nome'], "" ,uploaded_file,False)
				pes.save()
				threadProcessarFace(pes)
				messages.success(request, "Usuário cadastrado com sucesso!")
			elif data['nome'] != "" and data['check'] == False and data['codigo'] != "":
				pes = Pessoa.objects.create_Pessoa(data['nome'], data['codigo'] ,uploaded_file,False)
				pes.save()
				threadProcessarFace(pes)
				messages.success(request, "Usuário cadastrado com sucesso!")
			else:
				messages.error(request, "Algum campo não preenchido!")
			return render(request, 'formulario/cadastro_face.html')
		else:
			messages.error(request, "Algum campo não preenchido!")
	return render(request, 'formulario/cadastro_face.html')

@login_required(login_url='/')
def lista_cad(request):
	data = {}
	data['id'] = request.POST.get("id")
	data['pessoas'] = request.POST.get("pessoas")
	page_number = request.GET.get('page', 1)
	obj_per_page = 25
	if data['id']:
		return redirect("formulario_alterar", data['id'])
		#return render(request, 'formulario/alterar.html', {'id' : data['id']})
	elif data['pessoas']:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
		writer = csv.writer(response)
		writer.writerow(["id","nome","codigo","face_encoded","foto_valida", "bloqueado"])
		pessoas = Pessoa.objects.all()
		for p in pessoas:
			writer.writerow([p.id,p.nome,p.codigo,p.face_encoded,p.foto_valida, p.bloqueado])
		return response
	else:
		if request.method == 'POST':
			data['pesquisa'] = request.POST.get("search")
			if data['pesquisa'] == "":
				messages.error(request, "Campos da pesquisa não preenchidos!")
				pessoas = Pessoa.objects.all().order_by('id').reverse()
				paginator = Paginator(pessoas, obj_per_page)
				pessoas = paginator.get_page(page_number)
				return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})
			pessoas = Pessoa.objects.filter(nome__icontains=data['pesquisa'])
			if len(pessoas) == 0:
				pessoas = Pessoa.objects.all().order_by('id').reverse()
				paginator = Paginator(pessoas, obj_per_page)
				pessoas = paginator.get_page(page_number)
				messages.error(request, "Nenhum resultado encontrado!")
			return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})
		pessoas = Pessoa.objects.all().order_by('id').reverse()
		paginator = Paginator(pessoas, obj_per_page)
		pessoas = paginator.get_page(page_number)
		return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})

@login_required(login_url='/')
def lista_ace(request):
	data = {}
	data['acessos'] = request.POST.get("acessos")
	page_number = request.GET.get('page', 1)
	obj_per_page = 100
	if data['acessos']:
		acessos = Acesso.objects.select_related('fkPessoa').order_by('id').reverse()
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="entradas.csv"'
		writer = csv.writer(response)
		writer.writerow(["id","idpessoa", "nome","data","tipoAcesso"])
		for i in acessos:
			writer.writerow([i.id, i.fkPessoa, i.fkPessoa.nome, i.data, i.tipoAcesso])
		return response
	else:
		if request.method == 'POST':
			data['pesquisa'] = request.POST.get("search")
			data['dataIni'] = request.POST.get("dataI")
			data['dataFim'] = request.POST.get("dataF")
			if data['dataIni'] == "" and data['dataFim'] == "" and data['pesquisa'] == "":
				acessos = Acesso.objects.select_related('fkPessoa').order_by('id').reverse()
				paginator = Paginator(acessos, obj_per_page)
				acessos = paginator.get_page(page_number)
				messages.error(request, "Campos da pesquisa não preenchidos!")
				return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})
			if data['pesquisa'] == "":
				if data['dataFim'] != "":
					data['dataFim'] = datetime.datetime.strptime(data['dataFim'], '%Y-%m-%d')
					data['dataFim'] = data['dataFim'] + timedelta(days=1)
				else:
					data['dataFim'] = '8000-12-31'
				if data['dataIni'] != "":
					data['dataIni'] = datetime.datetime.strptime(data['dataIni'], '%Y-%m-%d')
				else:
					data['dataIni'] = '2000-01-01'
				acessos = Acesso.objects.select_related('fkPessoa').filter(data__range=[data['dataIni'],data['dataFim']]).order_by('id').reverse()
				if len(acessos) == 0:
					acessos = Acesso.objects.select_related('fkPessoa').order_by('id').reverse()
					messages.error(request, "Nenhum resultado encontrado!")
				paginator = Paginator(acessos, obj_per_page)
				acessos = paginator.get_page(page_number)
				return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})
			else:
				pessoas = Pessoa.objects.filter(nome__icontains=data['pesquisa'])
				if len(pessoas) == 0:
					messages.error(request, "Nenhum resultado encontrado!")
				else:
					if data['dataFim'] != "":
						data['dataFim'] = datetime.datetime.strptime(data['dataFim'], '%Y-%m-%d')
						data['dataFim'] = data['dataFim'] + timedelta(days=1)
					else:
						data['dataFim'] = '8000-12-31'
					if data['dataIni'] != "":
						data['dataIni'] = datetime.datetime.strptime(data['dataIni'], '%Y-%m-%d')
					else:
						data['dataIni'] = '2000-01-01'
					acessos = Acesso.objects.select_related('fkPessoa').filter(fkPessoa_id=pessoas[0].id).filter(data__range=[data['dataIni'],data['dataFim']]).order_by('id').reverse()
					if len(acessos) == 0:
						acessos = Acesso.objects.select_related('fkPessoa').order_by('id').reverse()
						messages.error(request, "Nenhum resultado encontrado!")
					paginator = Paginator(acessos, obj_per_page)
					acessos = paginator.get_page(page_number)
					return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})
	acessos = Acesso.objects.select_related('fkPessoa').order_by('id').reverse()
	paginator = Paginator(acessos, obj_per_page)
	acessos = paginator.get_page(page_number)
	return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})

@login_required(login_url='/')
def config(request):
	if request.method == 'POST':
		return render(request, 'formulario/configs.html')
	return render(request, 'formulario/configs.html')

@login_required(login_url='/')
def sobre(request):
	if request.method == 'POST':
		return render(request, 'formulario/sobre.html')
	return render(request, 'formulario/sobre.html')

@login_required(login_url='/')
def senha(request,):
	data = {}
	user = request.user
	if request.method == 'POST':
		data['senha1'] = request.POST.get("password")
		data['senha2'] = request.POST.get("password2")
		try:
			validate = password_validation.validate_password(data['senha1'])
			if data['senha1']  == data['senha2']:
				request.user.set_password(data['senha1'])
				user.save()
				user = authenticate(username=user, password=data['senha1'])
				auth_login(request,user)
				messages.success(request, "Senha alterada com sucesso!")
			else:
				messages.error(request, "As senhas inseridas não são iguais!")
		except Exception as e:
			for i in e:
				messages.error(request,str(i))
		return HttpResponseRedirect('/senha')
	return render(request, 'formulario/senha.html')

@login_required(login_url='/')
def alterar(request,idp):
	pessoa = Pessoa.objects.filter(id=idp)
	if request.method == 'POST':
		data = {}
		uploaded_file = ""
		if 'img' in request.FILES:
			uploaded_file = request.FILES['img']
		data['nome'] = request.POST.get("name")
		data['codigo'] = request.POST.get("code")
		data['bloqueado'] = bool(request.POST.get("checkbox"))
		if data['nome'] == "":
			messages.error(request, "Algum campo não preenchido!")
			return render(request, 'formulario/Alterar.html',{'pessoa' : pessoa})
		pes = Pessoa.objects.get(id=idp)
		pes.nome=data['nome']
		pes.codigo=data['codigo']
		pes.bloqueado=data['bloqueado']
		if uploaded_file != "":
			#image = ContentFile(uploaded_file)
			#im.save("media/"+str(uploaded_file))
			pes.foto.save(str(uploaded_file), uploaded_file, save=True)
		pes.save()
		if uploaded_file != "":
			threadProcessarFace(pes)
		return HttpResponseRedirect('/usuarioscadastrados')
		#return HttpResponseRedirect("UsuáriosCadastrados")
	return render(request, 'formulario/alterar.html',{'pessoa' : pessoa})

@csrf_protect
def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')
