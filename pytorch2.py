import os
import cv2
import numpy as np 
from tqdm import tqdm

REBUILD_DATA = True

class DogsVSCats(): 
    IMG_SIZE = 50 
    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    LABELS = {CATS: 0, DOGS: 1}
    training_data = []
    catcount = 0 
    dogcount = 0

    def maketrainingdata(self):
        for label in self.LABELS: 
            try:
                for f in tqdm(os.listdir(label)):
                    path = os.path.join(label, f)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
                    self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])

                    if label == self.CATS: 
                        self.catcount += 1
                    elif label == self.DOGS:
                        self.catcount += 1
            except Exception as e: 
                pass