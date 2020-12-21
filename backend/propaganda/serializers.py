from rest_framework import serializers
from .models import Propaganda

class PropagandaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Propaganda
        fields = ["id", "nome", "imagem", "genero",
        "exclusivo_cliente", "ativo", "fkFaixaEtaria"]
        depth = 1