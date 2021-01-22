from rest_framework import serializers
from .models import Pessoa
from .models import Acesso

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = '__all__'

class PessoaFaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = ('id', 'nome', 'codigo', 'face_encoded')

class PessoaListProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = ('id', 'foto', 'foto_processada')

class PessoaUpdateProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = ('id', 'face_encoded', 'foto_valida')


class PessoaApiFaceSerializer(serializers.ModelSerializer):

    imageBase64 = serializers.CharField(required=False)

    class Meta:
        model = Pessoa

        fields = ('id', 'nome', 'imageBase64', 'bloqueado', 'codigo')
        #fields = '__all__'


class AcessoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acesso
        fields = '__all__'
        #fields = ('cnpj', 'razaosocial')
        #read_only_fields = ( 'cnpj' ,)

    '''def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Acesso.objects.all()
        dataIni = self.request.query_params.get('dataIni', None)
        dataFim = self.request.query_params.get('dataFim', None)
        idpessoa = self.request.query_params.get('idpessoa', None)
        if idpessoa is not None:
            print(idpessoa)
            queryset = queryset.filter(acesso__fkPessoa=idpessoa)
        if dataIni is not None:
            queryset = queryset.filter(acesso__data__range=[dataIni, dataFim])
        return queryset'''


