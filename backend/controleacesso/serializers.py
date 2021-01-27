from rest_framework import serializers
from .models import Pessoa
from .models import Acesso
#from drf_extra_fields.fields import Base64ImageField

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

    #imageBase64 = Base64ImageField(required=False)

    class Meta:
        model = Pessoa

        fields = ('id', 'nome', 'foto', 'bloqueado', 'codigo')
        #fields = '__all__'

    def create(self, validated_data):
        #image = validated_data.pop('imageBase64')
        nome = validated_data.pop('nome')
        bloqueado = validated_data.pop('bloqueado')
        codigo = validated_data.pop('codigo')
        return Pessoa.objects.create(nome=nome, bloqueado=bloqueado, codigo=codigo,foto=image)


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


