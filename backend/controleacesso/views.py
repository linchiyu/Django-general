from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from django.core.files.base import ContentFile

from .models import Pessoa
from .models import Acesso
from .models import Totem
from .serializers import PessoaSerializer
from .serializers import PessoaFaceSerializer
from .serializers import PessoaApiFaceSerializer
from .serializers import AcessoSerializer
from .serializers import TotemSerializer

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

import datetime


######CRUD Pessoa#########
#create
class PessoaApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = PessoaSerializer

    def get_queryset(self):
        return Pessoa.objects.filter(fkEmpresa=self.request.user.funcionario.fkEmpresa)


######CRUD Acesso#########
#create
class AcessoApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = AcessoSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        p = serializer.validated_data.get('fkPessoa', None)
        if p:
            idade = int((datetime.date.today() - p.data_nascimento).days/365)
            serializer.save(genero=p.genero, idade=idade, fkTotem=self.request.user.totem)
        else:
            serializer.save(fkTotem=self.request.user.totem)

    def get_queryset(self):
        return Acesso.objects.filter(fkTotem__user__funcionario__fkEmpresa=self.request.user.funcionario.fkEmpresa)


######CRUD Totem#########
#create
class TotemApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Totem.objects.all()
    serializer_class = TotemSerializer

    