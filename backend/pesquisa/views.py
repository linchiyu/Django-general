from django.shortcuts import render
from rest_framework import generics

from .models import Satisfacao

from .serializers import SatisfacaoSerializer

from rest_framework.permissions import IsAuthenticated
# Create your views here.

class SatisfacaoApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = SatisfacaoSerializer

    def perform_create(self, serializer):
           serializer.save(fkTotem=self.request.user.totem)

    def get_queryset(self):
        return Satisfacao.objects.filter(fkTotem__user__funcionario__fkEmpresa=self.request.user.funcionario.fkEmpresa)
