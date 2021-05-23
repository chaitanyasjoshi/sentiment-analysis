'''
Created on 21-Nov-2020

@author: Ghoongurde
'''
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

from sklearn.model_selection._split import train_test_split
import pickle
from twisted.python.util import println

from nltk.tokenize import RegexpTokenizer

import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from concurrent import futures

from sklearn import metrics



stop_words = set(stopwords.words('english'))


#print(stop_words)

filename = "best_model.sav"

prev_res = 0.0

token = RegexpTokenizer(r'[a-zA-Z0-9]+')

text_pip = Pipeline([('vect', CountVectorizer(stop_words=ENGLISH_STOP_WORDS, ngram_range=(1,1), tokenizer = token.tokenize)), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])


print("Before Read")
amazon = pd.read_csv("amazon.csv", usecols=["reviews.rating", "reviews.text"], encoding="ISO-8859-15")
print("After Read")

sentiment = []
for i in range(len(amazon["reviews.rating"])):
    if(amazon["reviews.rating"].values[i].astype("int") >= 0 and amazon["reviews.rating"].values[i].astype("int") < 3):
        sentiment.append("0")
    elif(amazon["reviews.rating"].values[i].astype("int") == 3):
        sentiment.append("1")
    else:
        sentiment.append("2")
       
amazon.insert(2, "sentiments", sentiment, True)
        

train = []
test = []




#for i in range(1, 100):

train, test = train_test_split(amazon, test_size=0.3, shuffle=True)

text_pip = text_pip.fit(train.values[:, 1], train["sentiments"].values[:].astype("int"))

res = text_pip.score(test.values[:, 1], test["sentiments"].values[:].astype("int"))

println("Acc.: " + str(res))# + "------------------------ iteration " + str(i))


if(res > prev_res):
    pickle.dump(text_pip, open(filename, 'wb'))
    print("(New Best)")
    prev_res = res
#text_pip = pickle.load(open(filename, 'rb'))

loaded_model = pickle.load(open(filename, 'rb'))
preds = loaded_model.predict(test.values[:, 1])

res = loaded_model.score(test.values[:, 1], test["sentiments"].values[:].astype("int"))

println("Loaded model score: " + str(res))

##CONFUSION MATRIX AND METRICS
print(metrics.confusion_matrix(test['sentiments'].values[:].astype("int"), preds))
print(metrics.classification_report(test['sentiments'].values[:].astype("int"), preds))

while True:
    lists = []
    print("Do you want to enter a review?")
    new_str = input()
    if new_str == 'n':
        break
    else:
        print("Enter a string review: ")
        new_str = input()
        lists.append(new_str)
        print("Result: " + str(loaded_model.predict(lists)[0]))
        
with open('output.csv', 'w+', encoding='utf-8') as file:
    fieldnames = ['reviews', 'pred_rating']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    for j in range(len(preds)):
        writer.writerow({'reviews': test.values[j, 1], 'pred_rating': preds[j]})
