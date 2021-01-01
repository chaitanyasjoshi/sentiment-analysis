'''
Created on 22-Nov-2020

@author: Chaitanya Joshi
'''
import pickle

filename = "../training/best_model.sav"

def init():
    global model
    model = pickle.load(open(filename, 'rb'))

def predict(reviews):
    init()
    new_reviews = []
    for review in reviews:
        review = review.lower()
        new_reviews.append(review)
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
    