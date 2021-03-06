from django.db import models
from PIL import Image
# Create your models here.

class PessoaManager(models.Manager):
    def create_Pessoa(self,nome,codigo,foto,bloqueado):
        pessoa = self.create(nome=nome,codigo=codigo,foto=foto,bloqueado=bloqueado)
        return pessoa

class Pessoa(models.Model):
    class Meta:
        db_table = 'pessoa'
    nome = models.CharField(max_length=40)
    codigo = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField()
    face_encoded = models.CharField(max_length=3500, blank=True, null=True)
    foto_valida = models.BooleanField(default=False)
    foto_processada = models.BooleanField(default=False)
    bloqueado = models.BooleanField(default=False)

    objects = PessoaManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        im = Image.open(self.foto)
        #set maxsize of the image
        im.thumbnail( (700,700) )
        im.save(self.foto.path)

        im.close()

        super(Pessoa,self).save()

class Acesso(models.Model):
    class Meta:
        db_table = 'acesso'
    data = models.DateTimeField()
    tipoAcesso = models.CharField(max_length=10) #0 = entrada 1 = saida
    fkPessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)
