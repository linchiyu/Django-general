from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Server(models.Model):
    class Meta:
        db_table = 'server'
    name = models.CharField(max_length=40)
    ip = models.CharField(max_length=50, default='127.0.0.1')
    port = models.PositiveSmallIntegerField(default=50000)
    authkey = models.BinaryField(max_length=40, default=b'articfoxmemoryauthkey')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_by')

    def __str__(self):
        return str(self.id)+' - '+str(self.name)

class Camera(models.Model):
    class Meta:
        db_table = 'camera'

    name = models.CharField(max_length=40)
    memory_name = models.CharField(max_length=40, unique=True, blank=True)
    #momory name can be name with: re.sub('[^A-Za-z0-9]+', '', name+id)
    configuration = models.TextField(max_length=500, 
    	default='''{
"ip": "",
"port": "",
"user": "",
"password": ""
}''')
    active = models.BooleanField(default=True)
    fkserver = models.ForeignKey(Server, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Camera_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Camera_updated_by')

    def __str__(self):
        return str(self.id)+' - '+str(self.name)