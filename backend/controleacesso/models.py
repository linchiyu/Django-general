from django.db import models
from django.contrib.auth.models import User
from autenticacao.models import Empresa

# Create your models here.
class PessoaManager(models.Manager):
    def create_Pessoa(self,nome,foto,bloqueado):
        pessoa = self.create(nome=nome,foto=foto)
        return pessoa

GENDER_CHOICES = (
        (0, 'Feminino'),
        (1, 'Masculino'),
        (2, 'Não especificado'),
    )

class Totem(models.Model):
    class Meta:
        db_table = 'totem'
    nome = models.CharField(max_length=40)
    descricao = models.TextField(blank=True)
    configuracao = models.TextField(blank=True)
    token = models.CharField(blank=True, max_length=80)

    ativo = models.BooleanField(default=True)

    fkEmpresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Totem_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Totem_updated_by')

    def __str__(self):
        return str(self.id)

class Pessoa(models.Model):
    class Meta:
        db_table = 'pessoa'
    nome = models.CharField(max_length=40)
    foto = models.ImageField()
    foto_valida = models.BooleanField(default=False)
    data_nascimento = models.DateField()
    genero = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    face_encoded = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    fkEmpresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Pessoa_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Pessoa_updated_by')

    objects = PessoaManager()

    def __str__(self):
        return str(self.id)

class Acesso(models.Model):
    class Meta:
        db_table = 'acesso'
    data = models.DateTimeField()
    fkpessoa = models.ForeignKey(Pessoa, blank=True, null=True, on_delete=models.PROTECT)
    genero = models.PositiveSmallIntegerField(blank=True, null=True, choices=GENDER_CHOICES)
    idade = models.PositiveSmallIntegerField(blank=True, null=True)

    fkEmpresa = models.ForeignKey(Totem, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
