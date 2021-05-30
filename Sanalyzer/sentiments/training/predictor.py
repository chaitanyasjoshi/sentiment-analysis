'''
Created on 22-Nov-2020

@author: Chaitanya Joshi
'''
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import multiprocessing
from joblib import Parallel, delayed
import re

num_cores = multiprocessing.cpu_count()

filename1 = "../training/model_1.sav"
filename2 = "../training/model_2.sav"
filename3 = "../training/model_3.sav"
vect1 = "../training/tfidf1.sav"
vect2 = "../training/tfidf2.sav"
vect3 = "../training/tfidf3.sav"

def parallel_clean(data):
    s2 = data.strip().lower()
    temp_text = re.sub(r'[^\w\ss2]', '', s2)
                #print("Iteration " + str(i))

    return temp_text

def init():
    global model, tfidf
    model = []
    tfidf = []
    model.append(pickle.load(open(filename1, 'rb')))
    model.append(pickle.load(open(filename2, 'rb')))
    model.append(pickle.load(open(filename3, 'rb')))
    tfidf.append(pickle.load(open(vect1, 'rb')))
    tfidf.append(pickle.load(open(vect2, 'rb')))
    tfidf.append(pickle.load(open(vect3, 'rb')))

def predict(model_index, reviews):
    init()
    new_reviews = []
    #for review in reviews:      
    new_reviews = Parallel(n_jobs=-1, backend="threading")(map(delayed(parallel_clean), reviews))
    new_reviews = tfidf[model_index].transform(new_reviews)
    
    preds = model[model_index].predict(new_reviews)
    return preds



#while(1):
#    print("Do you want to enter another review?: ")
#    ip = input()
#    if ip == 'n':
#        break
#    
#    print("Enter string review: ")
#    rev = input()
#    print(rev)
#    print(str(predict(rev)))
    