from django.db import models
from controleacesso.models import Totem


EMOTION_CHOICES = (
        (0, 'raiva'),
        (1, 'nojo'),
        (2, 'medo'),
        (3, 'alegria'),
        (4, 'tristeza'),
        (5, 'surpresa'),
        (6, 'neutro'),
    )
        

# Create your models here.
class Satisfacao(models.Model):
    class Meta:
        db_table = 'satisfacao'
    data = models.DateTimeField()
    emocao = models.PositiveSmallIntegerField(choices=EMOTION_CHOICES)

    fkEmpresa = models.ForeignKey(Totem, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)