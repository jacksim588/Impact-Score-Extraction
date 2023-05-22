import pickle
import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

class Categoriser:
    
    def __init__(self,tokenizer,text_labels,model_pl1):
        self.tokenizer = tokenizer
        self.text_labels = text_labels
        self.model_pl1 = model_pl1



    def pl1_categorisation(self,text):
        x = self.tokenizer.texts_to_matrix([text])
        pred = self.model_pl1.predict(x)
        return (self.text_labels[np.argmax(pred[0])])
    


