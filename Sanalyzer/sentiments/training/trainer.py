'''
Created on 21-Nov-2020

@author: Chaitanya Joshi
'''
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection._split import train_test_split
import pickle
from twisted.python.util import println
from sklearn.ensemble.forest import RandomForestClassifier
from nltk.tokenize import RegexpTokenizer
from sklearn.svm import SVC
from nltk.stem import WordNetLemmatizer
import regex as re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem.porter import PorterStemmer

stop_words = set(stopwords.words('english'))

#print(stop_words)

filename = "best_model.sav"

prev_res = 0.0

token = RegexpTokenizer(r'[a-zA-Z0-9]+')

text_pip = Pipeline([('vect', CountVectorizer(stop_words=ENGLISH_STOP_WORDS, ngram_range=(1,1), tokenizer = token.tokenize)), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])


print("Before Read")
amazon = pd.read_csv("training.1600000.processed.noemoticon.csv", header=None, names=["target", "ids", "date", "flag", "user", "text"], usecols=["target", "text"], encoding="ISO-8859-15")
print("After Read")
#sentiment = []

#for i in range(len(amazon["reviews.rating"])):
#    if(amazon["reviews.rating"].values[i].astype("int") >= 0 and amazon["reviews.rating"].values[i].astype("int") < 3):
#        sentiment.append("0")
#    elif(amazon["reviews.rating"].values[i].astype("int") == 3):
#        sentiment.append("1")
#    else:
#        sentiment.append("2")
       
#amazon.insert(2, "sentiment", sentiment, True)
        

train = []
test = []



for i in range(1, 100):

    train, test = train_test_split(amazon, test_size=0.1, shuffle=True)
    
    
        
    #X = amazon["reviews.text"]
    #Y = amazon["reviews.rating"].astype("int")
    
    #for i in range(1, 5):
    
    #lemma = WordNetLemmatizer()
    #stemmer = PorterStemmer()
    
    #for sen in range(0, len(train)):
        # Remove all the special characters
    #    document = re.sub(r'\W', ' ', str(train["text"].values[sen]))
        
        # remove all single characters
    #    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        
        # Remove single characters from the start
    #    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        
        # Substituting multiple spaces with single space
    #    document = re.sub(r'\s+', ' ', document, flags=re.I)
        
        # Removing prefixed 'b'
    #    document = re.sub(r'^b\s+', '', document)
        
        # Converting to Lowercase
    #    document = document.lower()
        
        # Lemmatization
    #    document = document.split()
    
    #    document = [lemma.lemmatize(word) for word in document]
    #    document = [stemmer.stem(word) for word in document]
    #    document = ' '.join(document)
        
    #    documents.append(document)
    
    text_pip = text_pip.fit(train.values[:, 1], train["target"].values[:].astype("int"))
    
    #preds = text_pip.predict(test.values[:, 1])
    
    #trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.3, shuffle=True)
    
    #text_pip = text_pip.fit(trainX, trainY.values[:].astype("int"))
    
    res = text_pip.score(test.values[:, 1], test["target"].values[:].astype("int"))
    
    println("Acc.: " + str(res) + "------------------------ iteration " + str(i))
    if(res > prev_res):
        pickle.dump(text_pip, open(filename, 'wb'))
        print("(New Best)")
        prev_res = res
    #text_pip = pickle.load(open(filename, 'rb'))

loaded_model = pickle.load(open(filename, 'rb'))
preds = loaded_model.predict(test.values[:, 1])

res = loaded_model.score(test.values[:, 1], test["target"].values[:].astype("int"))

println("Loaded model score: " + str(res))

#println("TestX: " + str(len(testX)))
#println("Preds: " + str(len(preds)))
        
with open('output.csv', 'w+', encoding='utf-8') as file:
    fieldnames = ['reviews', 'pred_rating']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    for j in range(len(preds)):
        writer.writerow({'reviews': test.values[j, 1], 'pred_rating': preds[j]})
