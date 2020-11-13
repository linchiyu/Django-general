from django.shortcuts import render
from rest_framework import generics

from .models import Satisfacao

from .serializers import SatisfacaoSerializer

from rest_framework.permissions import IsAuthenticated
# Create your views here.

class SatisfacaoApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Satisfacao.objects.all()
    serializer_class = SatisfacaoSerializer