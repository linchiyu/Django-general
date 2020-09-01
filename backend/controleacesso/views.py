from django.shortcuts import render
from rest_framework import generics
from rest_framework import status

from .models import Pessoa
from .models import Acesso
from .serializers import PessoaSerializer
from .serializers import PessoaFaceSerializer
from .serializers import AcessoSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .logic import encodeFace
from threading import Thread


#call  t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
def processarFace(pessoa):
    encoded = encodeFace(pessoa.foto)
    pessoa.face_encoded = encoded
    pessoa.save()

######CRUD Pessoa#########
#create
class PessoaCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def post(self, request):
        serializer = PessoaSerializer(data=request.data)
        if serializer.is_valid():
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