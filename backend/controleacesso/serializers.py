from rest_framework import serializers
from .models import Pessoa
from .models import Acesso
from .models import Totem

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = '__all__'

class PessoaFaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = ('id', 'nome', 'face_encoded')


class PessoaApiFaceSerializer(serializers.ModelSerializer):

    imageBase64 = serializers.CharField(required=False)

    class Meta:
        model = Pessoa

        fields = ('id', 'nome', 'imageBase64', 'codigo')
        #fields = '__all__'


class AcessoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acesso
        #fields = '__all__'
        #fields = ('cnpj', 'razaosocial')
        read_only_fields = ('fkTotem',)
        exclude = ('created_at', )
        #depth = 1



class TotemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Totem
        fields = '__all__'
        #fields = ('cnpj', 'razaosocial')
        #read_only_fields = ( 'cnpj' ,)