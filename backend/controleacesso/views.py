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

from .logic import encodeFace
from threading import Thread

from PIL import Image
from io import BytesIO
import base64


#call  t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
def processarFace(pessoa):
    encoded = encodeFace(pessoa.foto)
    pessoa.face_encoded = encoded
    pessoa.save()

######CRUD Pessoa#########
#create
class PessoaApi(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer


######CRUD Acesso#########
#create
class AcessoApi(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    
    queryset = Acesso.objects.all()
    serializer_class = AcessoSerializer

######CRUD Totem#########
#create
class TotemApi(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    
    queryset = Totem.objects.all()
    serializer_class = TotemSerializer