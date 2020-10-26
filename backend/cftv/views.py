#django
from django.shortcuts import render
from django.http.response import StreamingHttpResponse

#models and serializers
from .models import Server, Camera
from .serializers import ServerSerializer, CameraSerializer

#rest
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

#mypackages
from .utils.memory import MemoryClass

#other
import time

#=======REST FRAMEWORK=========
class ServerList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filterset_fields = {
    }

class CameraList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    
    queryset = Camera.objects.filter(active=True)
    serializer_class = CameraSerializer
    filterset_fields = {
        #"fkpessoa": ['exact'],
    }

#=======VIDEO STREAM=========
def gen(mem):
    while True:
        time.sleep(0.05)
        frame = mem.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(memory_name):
    return StreamingHttpResponse(gen(MemoryClass(memory_name)), 
        content_type='multipart/x-mixed-replace; boundary=frame')