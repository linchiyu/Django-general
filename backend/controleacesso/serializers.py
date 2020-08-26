from rest_framework import serializers
from .models import Pessoa
from .models import Acesso

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Pessoa
        fields = '__all__'


class AcessoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Acesso
        fields = '__all__'
        #fields = ('cnpj', 'razaosocial')
        #read_only_fields = ( 'cnpj' ,)
