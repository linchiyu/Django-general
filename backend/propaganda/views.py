from django.shortcuts import render
from rest_framework import generics

from .models import Propaganda

from .serializers import PropagandaSerializer

from rest_framework.permissions import IsAuthenticated
# Create your views here.

class PropagandaApi(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    queryset = Propaganda.objects.all()
    serializer_class = PropagandaSerializer