from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np
from multiprocessing import shared_memory
import time

#models and serializers
from .models import Server, Camera
from .serializers import ServerSerializer, CameraSerializer

#django imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class MemoryClass():
    """docstring for Memory"""
    def __init__(self, memory_name):
        self.existing_shm = shared_memory.SharedMemory(name=memory_name)

    def __del__(self):
        self.existing_shm.close()

    def get_frame(self):
        image = np.ndarray((700,700,3), dtype=np.uint8, buffer=self.existing_shm.buf)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(mem):
    while True:
        time.sleep(0.05)
        frame = mem.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(memory_name):
    #return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(gen(MemoryClass(memory_name)), 
        content_type='multipart/x-mixed-replace; boundary=frame')