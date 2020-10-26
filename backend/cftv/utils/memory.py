#mypackages
from .managers import SharedMemoryManager

#others
import cv2
from multiprocessing import shared_memory
#import numpy as np

class ImageManager(SharedMemoryManager):
    pass

class MemoryClass():
    """Manage the shared memory"""
    def __init__(self, memory_name):
        self.camera = Camera.objects.get(memory_name=memory_name)
        self.server = Server.objects.get(id=self.camera.fkserver.id)

        ImageManager.register('getSharedMemory')
        self.smm = ImageManager(address=(self.server.ip, self.server.port), 
            authkey=self.server.authkey)
        self.smm.connect()

    def __del__(self):
        self.smm.shutdown()

    def get_frame(self):
        existing_shm = self.smm.getSharedMemory(name=self.camera.memory_name)
        image = existing_shm.copy()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()