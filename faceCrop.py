
import cv #Opencv
from PIL import Image#Image from PIL
from cv2 import *
import cv2
import glob
import os


def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Detect the faces
    faces = faceCascade.detectMultiScale(image, 1.3, 5)

    for ((x, y, w, h)) in faces:
        crop_image = image[y:y+h, x:x+w]
        cv2.imwrite("cropped.jpg", crop_image)
