from django.db import models

# Create your models here.
class Pessoa(models.Model):
    class Meta:
        db_table = 'pessoa'

    nome = models.CharField(max_length=40)
    codigo = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='rosto')
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Acesso(models.Model):
    class Meta:
        db_table = 'acesso'

    data = models.DateTimeField()
    tipoAcesso = models.CharField(max_length=10) #0 = entrada 1 = saida
    fkpessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)

    def __str__(self):
        return self.data
