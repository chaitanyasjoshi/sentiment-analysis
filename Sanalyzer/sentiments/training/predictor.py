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

filename = "../training/best_model.sav"
vect = "../training/tfidf.sav"

def parallel_clean(data):
    s2 = data.strip().lower()
    temp_text = re.sub(r'[^\w\ss2]', '', s2)
                #print("Iteration " + str(i))

    return temp_text

def init():
    global model, tfidf
    model = pickle.load(open(filename, 'rb'))
    tfidf = pickle.load(open(vect, 'rb'))

def predict(reviews):
    init()
    new_reviews = []
    #for review in reviews:      
    new_reviews = Parallel(n_jobs=-1, backend="threading")(map(delayed(parallel_clean), reviews))
    new_reviews = tfidf.transform(new_reviews)
    
    preds = model.predict(new_reviews)
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
    