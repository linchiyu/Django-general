import numpy as np
import json
from json import JSONEncoder
from threading import Thread
from django.conf import settings
import cv2


if settings.DEBUG:
    static = settings.STATIC_URL
else:
    static = settings.STATIC_ROOT

#face recognition modules
if settings.LOAD_RECOGNITION:
    import dlib
    from keras.preprocessing import image
    from . import Facenet
    face_detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('.'+static+"weights/shape_predictor_5_face_landmarks.dat")
    recog = Facenet.FaceNetClass()
    recog.loadModel()
    input_shape = recog.model.layers[0].input_shape
    if type(input_shape) == list:
        input_shape = input_shape[0][1:3]
    else:
        input_shape = input_shape[1:3]

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def encodeFace(path):
    #transforma imagem do PATH para um json com {"face": [128-D face points array]}
    try:
        img = cv2.imread(settings.MEDIA_ROOT+'/'+str(path))
        detections = face_detector(img)
        face_encoding = []
        if len(detections) > 0:
            img_shape = sp(img, detections[0])

            img = dlib.get_face_chip(img, img_shape, size = input_shape[0])
            #post processing
            img = cv2.resize(img, input_shape)

            img_pixels = image.img_to_array(img)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            img_pixels /= 255 #normalize input in [0, 1]

            face_encoding = recog.predict(img_pixels)[0,:]

        # Serialization
        numpyData = {"face": face_encoding}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
        #print("Printing JSON serialized NumPy array")
        #print(encodedNumpyData)
        return encodedNumpyData
    except:
        print("exception")
        raise
        return json.dumps({"face": []})

def getFaceArray(encodedNumpyData):
    #converte o json em array numpy
    # Deserialization
    #print("Decode JSON serialized NumPy array")
    decodedArrays = json.loads(encodedNumpyData)

    finalNumpyArray = np.asarray(decodedArrays["face"])
    #print("NumPy Array")
    #print(finalNumpyArray)
    return finalNumpyArray

#call  t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
def processarFace(pessoa):
    encoded = encodeFace(pessoa.foto)
    pessoa.face_encoded = encoded
    if len(encoded) > 300:
        pessoa.foto_valida = True
    else:
        pessoa.foto_valida = False
    pessoa.save()

def threadProcessarFace(pessoa):
    if settings.LOAD_RECOGNITION:
        t = Thread(target=processarFace, args=(pessoa,), daemon=True).start()