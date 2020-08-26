from django.shortcuts import render
from rest_framework import generics

from .models import Pessoa
from .models import Acesso
from .serializers import PessoaSerializer
from .serializers import AcessoSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

######CRUD Pessoa#########
#create
class PessoaCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

#list
class PessoaList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

#update
class PessoaUpdate(generics.RetrieveUpdateAPIView):
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