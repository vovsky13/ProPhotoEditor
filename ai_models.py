import cv2
import numpy as np
import dlib
from deepface import DeepFace
from rembg import remove, new_session

detector = dlib.get_frontal_face_detector()

def analyze_face(image):
    try:
        analysis = DeepFace.analyze(image, actions=['emotion', 'age', 'race'], enforce_detection=False)
        return analysis[0]
    except:
        return None

def detect_faces(image):
    gray = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2GRAY)
    faces = detector(gray, 1)
    return faces

def remove_background(image, model_type):
    session = new_session(model_type)
    return remove(image, session=session)