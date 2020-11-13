from rest_framework import serializers
from .models import Satisfacao

class SatisfacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Satisfacao
        fields = '__all__'