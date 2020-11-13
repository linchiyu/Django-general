from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    class Meta:
        db_table = 'empresa'

    nome = models.CharField(max_length=100)
        
    def __str__(self):
        return str(self.nome)

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fkEmpresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='updated_by')


class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'
        
    def __str__(self):
        return ''