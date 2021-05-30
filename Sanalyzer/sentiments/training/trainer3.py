'''
Created on 21-Nov-2020

@author: Ghoongurde
'''
import pandas as pd
import numpy as np
import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
#from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from numba import cuda, jit
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.model_selection._split import train_test_split
import pickle

import multiprocessing
from joblib import Parallel, delayed

from nltk.tokenize import RegexpTokenizer

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from concurrent import futures

from sklearn import metrics

from tqdm import tqdm

num_cores = multiprocessing.cpu_count()


def parallel_clean(data):
    s2 = data.strip().lower()
    temp_text = re.sub(r'[^\w\ss2]', '', s2)
                #print("Iteration " + str(i))

    return temp_text
        
    

@jit
def fit_model(clf, train_X, train_Y):
  clf.fit(train_X, train_Y)
  return clf


#print(stop_words)

filename = "model_3.sav"

prev_res = 0.0

tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.8, min_df=5, norm='l2', use_idf=True, stop_words=ENGLISH_STOP_WORDS)
#clf = svm.SVC(kernel='linear')
#clf = DecisionTreeClassifier()
clf = BernoulliNB()

#token = RegexpTokenizer(r'[a-zA-Z0-9]+')

#text_pip = Pipeline([('vect', CountVectorizer(stop_words=ENGLISH_STOP_WORDS, ngram_range=(1,1), tokenizer = token.tokenize)), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])


print("Before Read")
amazon = pd.read_csv("training.1600000.processed.noemoticon.csv", header=None, names=["sentiments", "ids", "date", "flag", "user", "uncleaned_text"], usecols=["sentiments", "uncleaned_text"], encoding="ISO-8859-15")
amazon = amazon.dropna()
print("After Read")

#sentiment = []
#if __name__ == "__main__":
inputs = tqdm(amazon['uncleaned_text'])
cleaned_text = Parallel(n_jobs=-1, verbose=2, backend="threading")(map(delayed(parallel_clean), inputs))
    
'''
if(amazon["reviews.rating"].values[i].astype("int") >= 0 and amazon["reviews.rating"].values[i].astype("int") < 3):
    sentiment.append("0")
elif(amazon["reviews.rating"].values[i].astype("int") == 3):
    sentiment.append("1")
else:
    sentiment.append("2")
'''

amazon.insert(2, "text", cleaned_text, True)
#amazon.insert(3, "sentiments", sentiment, True)
        

train = []
test = []




#for i in range(1, 100):

train, test = train_test_split(amazon, test_size=0.3)

#text_pip = text_pip.fit(train.values[:, 1], train["sentiments"].values[:].astype("int"))
print("Before train transform")
train_tfidf = tfidf.fit_transform(train["text"])
print("Before test transform")
test_tfidf = tfidf.transform(test["text"])
#result = np.all((train_tfidf == "0.0"))

print("Before Training")

classifier = fit_model(clf, train_tfidf, train["sentiments"].values[:].astype("int"))

print("After Training")                                                       

#res = text_pip.score(test.values[:, 1], test["sentiments"].values[:].astype("int"))
y_pred = classifier.predict(test_tfidf)



print("Confusion Matrix\n",confusion_matrix(test["sentiments"].values[:].astype("int"), y_pred))
print("\n")
print("Classification Report\n",classification_report(test["sentiments"].values[:].astype("int"),y_pred))
print("\n")
res = accuracy_score(test["sentiments"].values[:].astype("int"),y_pred)*100
print("Accuracy : ",accuracy_score(test["sentiments"].values[:].astype("int"),y_pred)*100)


if(res > prev_res):
    pickle.dump(classifier, open(filename, 'wb'))
    print("(New Best)")
    prev_res = res
#text_pip = pickle.load(open(filename, 'rb'))

loaded_model = pickle.load(open(filename, 'rb'))
#preds = loaded_model.predict(test.values[:, 1])

#res = loaded_model.score(test.values[:, 1], test["sentiments"].values[:].astype("int"))
preds = loaded_model.predict(test_tfidf)

print("Loaded model score: " + str(res))

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
        lists = tfidf.transform(lists)
        print("Result: " + str(loaded_model.predict(lists)[0]))
        
with open('output.csv', 'w+', encoding='utf-8') as file:
    fieldnames = ['reviews', 'pred_rating']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    for j in range(len(preds)):
        writer.writerow({'reviews': test.values[j, 1], 'pred_rating': preds[j]})
