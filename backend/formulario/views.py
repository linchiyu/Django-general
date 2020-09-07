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
from controleacesso.logic import encodeFace
from rest_framework import serializers
import datetime
from datetime import timedelta
from PIL import Image
from django.contrib.auth import password_validation
import csv
from django.http import HttpResponse
from threading import Thread

# Create your views here.

#call  t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
def processarFace(pessoa):
    encoded = encodeFace(pessoa.foto)
    pessoa.face_encoded = encoded
    pessoa.save()

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
				t = Thread(target=processarFace, args=(pes,), daemon=True).start()
				messages.success(request, "Usuário cadastrado com sucesso!")
			elif data['nome'] != "" and data['check'] == False and data['codigo'] != "":
				pes = Pessoa.objects.create_Pessoa(data['nome'], data['codigo'] ,uploaded_file,False)
				pes.save()
				t = Thread(target=processarFace, args=(pes,), daemon=True).start()
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
	if data['id']:
		return redirect("formulario_alterar", data['id'])
		#return render(request, 'formulario/alterar.html', {'id' : data['id']})
	elif data['pessoas']:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
		writer = csv.writer(response)
		writer.writerow(["id","nome","codigo","face_encoded","bloqueado"])
		pessoas = Pessoa.objects.all()
		for p in pessoas:
			writer.writerow([p.id,p.nome,p.codigo,p.face_encoded,p.bloqueado])
		return response
	else:
		if request.method == 'POST':
			data['pesquisa'] = request.POST.get("search")
			if data['pesquisa'] == "":
				messages.error(request, "Campos da pesquisa não preenchidos!")
				pessoas = Pessoa.objects.all()
				return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})
			pessoas = Pessoa.objects.filter(nome=data['pesquisa'])
			if len(pessoas) == 0:
				pessoas = Pessoa.objects.all()
				messages.error(request, "Nenhum resultado encontrado!")
			return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})
		pessoas = Pessoa.objects.all()
		return render(request, 'formulario/lista_cadastrados.html', {'pessoas' : pessoas})

@login_required(login_url='/')
def lista_ace(request):
	data = {}
	data['acessos'] = request.POST.get("acessos")
	if data['acessos']:
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="entradas.csv"'
		aux = []
		acessosID =  data['acessos'].split(" ")
		for i in range(len(acessosID) +1):
			if i%2 != 0 and i != 1:
				aux.append(acessosID[i -1].split(">")[0])
		acessosID = aux
		writer = csv.writer(response)
		writer.writerow(["id","fkpessoa.nome","data","tipoAcesso"])
		for i in acessosID:
			acessos = Acesso.objects.select_related('fkpessoa').filter(id=i)
			writer.writerow([acessos[0].id,acessos[0].fkpessoa.nome,acessos[0].data,acessos[0].tipoAcesso])
		return response
	else:
		if request.method == 'POST':
			data['pesquisa'] = request.POST.get("search")
			data['dataIni'] = request.POST.get("dataI")
			data['dataFim'] = request.POST.get("dataF")
			if data['dataIni'] == "" and data['dataFim'] == "" and data['pesquisa'] == "":
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
				acessos = Acesso.objects.select_related('fkpessoa').filter(data__range=[data['dataIni'],data['dataFim']])
				if len(acessos) == 0:
					acessos = Acesso.objects.select_related('fkpessoa')
					messages.error(request, "Nenhum resultado encontrado!")
				return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})
			else:
				pessoas = Pessoa.objects.filter(nome=data['pesquisa'])
				if len(pessoas) == 0:
					acessos = Acesso.objects.select_related('fkpessoa')
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
					acessos = Acesso.objects.select_related('fkpessoa').filter(fkpessoa_id=pessoas[0].id).filter(data__range=[data['dataIni'],data['dataFim']])
					if len(acessos) == 0:
						acessos = Acesso.objects.select_related('fkpessoa')
						messages.error(request, "Nenhum resultado encontrado!")
					return render(request, 'formulario/lista_acessos.html', {'acessos' : acessos})
	acessos = Acesso.objects.select_related('fkpessoa')
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
		if uploaded_file == "":
			pes = Pessoa.objects.filter(id=idp).update(nome=data['nome'],codigo=data['codigo'],bloqueado=data['bloqueado'])
		if uploaded_file != "":
			im = Image.open(uploaded_file)
			im.save("media/"+str(uploaded_file))
			pes = Pessoa.objects.filter(id=idp).update(nome=data['nome'],codigo=data['codigo'],foto=uploaded_file,bloqueado=data['bloqueado'])
		return HttpResponseRedirect('/usuarioscadastrados')
		#return HttpResponseRedirect("UsuáriosCadastrados")
	return render(request, 'formulario/alterar.html',{'pessoa' : pessoa})

@csrf_protect
def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')
