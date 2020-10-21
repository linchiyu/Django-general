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
from .utils.managers import SharedMemoryManager

#other
import cv2
import numpy as np
from multiprocessing import shared_memory
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

class ImageManager(SharedMemoryManager):
    pass

#=======VIDEO STREAM=========
class MemoryClass():
    """docstring for Memory"""
    def __init__(self, memory_name):
        self.camera = Camera.objects.get(memory_name=memory_name)
        self.server = Server.objects.get(id=self.camera.fkserver.id)

        ImageManager.register('getSharedMemory')
        self.smm = ImageManager(address=(self.server.ip, self.server.port), 
            authkey=self.server.authkey)
        self.smm.connect()

        #self.existing_shm = self.smm.getSharedMemory(name=memory_name)
        #self.existing_shm = shared_memory.SharedMemory(name=memory_name)
        #existing_shm = smm.getSharedMemory()

    def __del__(self):
        self.smm.shutdown()

    def get_frame(self):
        existing_shm = self.smm.getSharedMemory(name=self.camera.memory_name)
        image = existing_shm.copy()
        #image = np.ndarray((700,700,3), dtype=np.uint8, buffer=self.existing_shm.buf)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(mem):
    while True:
        time.sleep(0.05)
        frame = mem.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(memory_name):
    return StreamingHttpResponse(gen(MemoryClass(memory_name)), 
        content_type='multipart/x-mixed-replace; boundary=frame')