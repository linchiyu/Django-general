from django.db import models
from autenticacao.models import Empresa
from django.contrib.auth.models import User

# Create your models here
class FaixaEtaria(models.Model):
    class Meta:
        db_table = 'faixaEtaria'
        verbose_name_plural = 'Faixas Etarias'


    nome = models.CharField(max_length=40)
    idade_minima = models.PositiveSmallIntegerField()
    idade_maxima = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.nome

class Propaganda(models.Model):
    GENDER_CHOICES = (
        (0, 'Feminino'),
        (1, 'Masculino'),
        (2, 'Não especificado'),
    )

    class Meta:
        db_table = 'propaganda'

    nome = models.CharField(max_length=40)
    imagem = models.ImageField()
    genero = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    ativo = models.BooleanField(default=True)
    fkFaixaEtaria = models.ForeignKey(FaixaEtaria, on_delete=models.PROTECT)
    fkEmpresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Propaganda_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Propaganda_updated_by')
    
    def __str__(self):
        return self.nome