import face_recognition
import numpy as np
import json
from json import JSONEncoder
from threading import Thread
from django.conf import settings
import cv2

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def encodeFace(path):
    #transforma imagem do PATH para um json com {"face": [128-D face points array]}
    try:
        image = face_recognition.load_image_file(settings.MEDIA_ROOT+'/'+str(path))
        face_encoding = face_recognition.face_encodings(image)[0]

        # Serialization
        numpyData = {"face": face_encoding}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
        #print("Printing JSON serialized NumPy array")
        #print(encodedNumpyData)
        return encodedNumpyData
    except:
        print("exception")
        return json.dumps({"face": []})


def threadFaceEncoding(path):
    t = Thread(target=encodeFace, args=(path,), daemon=True).start()


def getFaceArray(encodedNumpyData):
    #converte o json em array numpy
    # Deserialization
    #print("Decode JSON serialized NumPy array")
    decodedArrays = json.loads(encodedNumpyData)

    finalNumpyArray = np.asarray(decodedArrays["face"])
    #print("NumPy Array")
    #print(finalNumpyArray)
    return finalNumpyArray
