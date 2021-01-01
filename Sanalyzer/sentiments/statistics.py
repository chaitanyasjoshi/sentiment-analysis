'''
Created on 22-Nov-2020

@author: Chaitanya Joshi
'''

from Sanalyzer.sentiments.training import predictor

def stats(reviews):
    noPos = 0
    noNeg = 0
    noTotal = len(reviews)
    preds = predictor.predict(reviews)
    for pred in preds:
        if pred == 0:
            noNeg += 1
        elif pred == 4:
            noPos += 1
                    
    perPos = (noPos * 100)/noTotal;
    perNeg = (noNeg * 100)/noTotal;
    
    return noTotal, noPos, noNeg, perPos, perNeg