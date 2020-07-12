import cv2
import numpy as np 
import pytesseract


def changeimg():
    img = cv2.imread("canvas.png")
    text = pytesseract.image_to_string(img)
    return text