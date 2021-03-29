from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from django.core.files.base import ContentFile

from .models import Pessoa
from .models import Acesso
from .serializers import PessoaSerializer
from .serializers import PessoaFaceSerializer
from .serializers import PessoaApiFaceSerializer
from .serializers import PessoaApiFaceB64Serializer
from .serializers import PessoaApiPartialUpdateB64Serializer
from .serializers import PessoaListProcessSerializer
from .serializers import PessoaUpdateProcessSerializer
from .serializers import AcessoSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .logic import threadProcessarFace
from threading import Thread

from PIL import Image
from io import BytesIO
import base64


######CRUD Pessoa#########
#create
class PessoaApiCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaApiFaceSerializer

    def post(self, request):
        serializer = PessoaApiFaceSerializer(data=request.data)
        if serializer.is_valid():
            #image = ContentFile(base64.b64decode(serializer.data['imageBase64']))

            '''pessoa = Pessoa(nome=serializer.data['nome'], 
                codigo=serializer.data['codigo'],
                bloqueado=serializer.data['bloqueado'])
            pessoa.foto.save('api.jpg', image, save=True)
            pessoa.save()'''
            pessoa = serializer.save()

            threadProcessarFace(pessoa)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PessoaApiCreateB64(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaApiFaceB64Serializer

    def post(self, request):
        serializer = PessoaApiFaceB64Serializer(data=request.data)
        if serializer.is_valid():
            #image = ContentFile(base64.b64decode(serializer.data['imageBase64']))

            '''pessoa = Pessoa(nome=serializer.data['nome'], 
                codigo=serializer.data['codigo'],
                bloqueado=serializer.data['bloqueado'])
            pessoa.foto.save('api.jpg', image, save=True)
            pessoa.save()'''
            pessoa = serializer.save()

            threadProcessarFace(pessoa)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#list people 128-D faces
class PessoaFace(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.filter(bloqueado=False, foto_valida=True).exclude(
        face_encoded__isnull=True).values('id', 'nome', 'codigo', 'face_encoded')
    serializer_class = PessoaFaceSerializer


#list
class PessoaList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    filterset_fields = {
        "id": ['exact'],
        "nome": ['contains'],
        "codigo": ['exact'],
        "bloqueado": ['exact'],
    }

class PessoaProcessList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.filter(bloqueado=False, foto_processada=False)
    serializer_class = PessoaListProcessSerializer


#update
class PessoaUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def put(self, request, pk):
        pessoa = Pessoa.objects.get(id=pk)
        serializer = PessoaSerializer(pessoa, data=request.data, partial=True)
        image_str = serializer.initial_data.get('foto', None)
        if serializer.is_valid():
            
            serializer.save()

            if image_str != None and image_str != '':
                threadProcessarFace(pessoa)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PessoaUpdateB64(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaApiPartialUpdateB64Serializer

    def put(self, request, pk):
        pessoa = Pessoa.objects.get(id=pk)
        serializer = PessoaApiPartialUpdateB64Serializer(pessoa, data=request.data, partial=True)
        image_str = serializer.initial_data.get('fotoBase64', None)
        if serializer.is_valid():
            
            serializer.save()

            if image_str != None and image_str != '':
                threadProcessarFace(pessoa)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PessoaProcessUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaUpdateProcessSerializer

    def put(self, request, pk):
        serializer = PessoaUpdateProcessSerializer(data=request.data)
        if serializer.is_valid():

            pessoa = Pessoa.objects.get(id=pk)
            pessoa.face_encoded = serializer.data['face_encoded']
            pessoa.foto_valida = serializer.data['foto_valida']
            pessoa.foto_processada = True

            pessoa.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PessoaRetrieve(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer


######CRUD Acesso#########
#create
class AcessoCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Acesso.objects.all()
    serializer_class = AcessoSerializer


#list
class AcessoList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Acesso.objects.all()
    serializer_class = AcessoSerializer
    filterset_fields = {
        "fkPessoa": ['exact'],
        "data": ['gte', 'lte'],
        "tipoAcesso": ['exact'],
    }