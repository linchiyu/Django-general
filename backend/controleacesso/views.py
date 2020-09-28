from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from django.core.files.base import ContentFile

from .models import Pessoa
from .models import Acesso
from .serializers import PessoaSerializer
from .serializers import PessoaFaceSerializer
from .serializers import PessoaApiFaceSerializer
from .serializers import AcessoSerializer

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
class PessoaApiCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaApiFaceSerializer

    def post(self, request):
        serializer = PessoaApiFaceSerializer(data=request.data)
        if serializer.is_valid():
            image = ContentFile(base64.b64decode(serializer.data['imageBase64']))

            pessoa = Pessoa.objects.create(nome=serializer.data['nome'], 
                codigo=serializer.data['codigo'],
                bloqueado=serializer.data['bloqueado'])
            pessoa.foto.save(str(pessoa.id)+'.jpg', image, save=True)

            t = Thread(target=processarFace, args=(pessoa,), daemon=True).start()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#deprecated
class PessoaCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def post(self, request):
        serializer = PessoaSerializer(data=request.data)
        if serializer.is_valid():
            print(type(serializer.validated_data['foto']))
            novaPessoa = serializer.save()
            t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#list people 128-D faces
class PessoaFace(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.filter(bloqueado=False).exclude(face_encoded__isnull=True).values('id', 'nome', 'codigo', 'face_encoded')
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

#update
class PessoaUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaApiFaceSerializer

    def put(self, request, pk):
        serializer = PessoaApiFaceSerializer(data=request.data)
        if serializer.is_valid():
            image = ContentFile(base64.b64decode(serializer.data['imageBase64']))

            pessoa = Pessoa.objects.get(id=pk)
            pessoa.nome = serializer.data['nome']
            pessoa.codigo = serializer.data['codigo']
            pessoa.bloqueado = serializer.data['bloqueado']

            pessoa.foto.save(str(pessoa.id)+'.jpg', image, save=True)
            pessoa.save()

            t = Thread(target=processarFace, args=(pessoa,), daemon=True).start()
            
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
        "fkpessoa": ['exact'],
        "data": ['gte', 'lte'],
        "tipoAcesso": ['exact'],
    }