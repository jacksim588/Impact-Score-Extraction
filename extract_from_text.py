
import pandas as pd
import numpy as np
import categorisation
import pickle
import numpy as np
import re
import csv
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from sharepoint import SharePoint
from supporting_files import get_supporting_files
from OCR import ocr_image


def get_pl1(text,c1):
    return c1.pl1_categorisation(text)

def get_ingredients(text,ingredients_set):
    text=str(text)
    return(list( dict.fromkeys(re.findall(r"\b(" + "|".join((ingredients_set)) + r")\b", text.lower()) )))

def get_lifestyles(text, lifestyles_set):
    text=str(text)
    return(list( dict.fromkeys(re.findall(r"\b(" + "|".join((lifestyles_set)) + r")\b", text.lower()) )))

def get_ingredients_set():
    ingredients_set=set()
    with open("Supporting Files\Ingredients.csv", "r", encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                ingredients_set.add(row[0])
            except IndexError:
                pass
    return ingredients_set


def get_lifestyles_set():
    lifestyles_set=set()
    with open("Supporting Files\Lifestyles.csv", "r", encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                lifestyles_set.add(row[0])
            except IndexError:
                pass
    lifestyles_set = map(str.lower, lifestyles_set)
    return lifestyles_set

def create_categoriser():

    with open(r'Supporting Files\Model Files\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    model_pl1 = load_model(r'Supporting Files\Model Files\model_0.1.h5')
    np_load_old = np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    encoder = LabelEncoder()
    encoder.classes_ = np.load(r'Supporting Files\Model Files\classes.npy')
    text_labels = encoder.classes_


    c1=categorisation.Categoriser(tokenizer=tokenizer,text_labels=text_labels,model_pl1=model_pl1)
    return c1


def get_nutritional_info(text):
    keywords = ['sugars', 'fat', 'saturates', 'salt']
    info = {}

    for keyword in keywords:
        pattern = r"{} ([0-9.]+)g".format(keyword)
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            info[keyword] = str(value)

    return info



