import pickle
import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

class Categoriser:
    
    def __init__(self,tokenizer,text_labels,model):
        self.tokenizer = tokenizer
        self.text_labels = text_labels
        self.model = model



    def classify(self,text):
        x = self.tokenizer.texts_to_matrix([text])
        pred = self.model.predict(x)
        return (self.text_labels[np.argmax(pred[0])])
    


    


