from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np
from multiprocessing import shared_memory
import time

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

class Memory():
    """docstring for Memory"""
    def __init__(self):
        self.existing_shm = shared_memory.SharedMemory(name='cameraframe')

    def __del__(self):
        self.existing_shm.close()

def gen2(mem):
    while True:
        time.sleep(0.05)
        image = np.ndarray((720,1280,3), dtype=np.uint8, buffer=mem.existing_shm.buf)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream():
    #return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(gen2(Memory()), 
        content_type='multipart/x-mixed-replace; boundary=frame')