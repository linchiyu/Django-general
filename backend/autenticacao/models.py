from django.db import models

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'


    def __str__(self):
        return ''