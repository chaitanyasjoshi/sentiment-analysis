'''
Created on 23-Nov-2020

@author: Chaitanya Joshi
'''
from Sanalyzer.sentiments import statistics as stat
import csv
import os
import json

filename = 'reviews.csv'

def calc():
    if os.path.exists('sentiments.json'):
        os.remove('sentiments.json')
    reviews = []
    sentiments = { 'data': []}
    with open(filename, 'r', encoding="utf-8") as data:
        for line in csv.reader(data):
            reviews.append(str(line))
            
    print(len(reviews))
    noTotal_1, noPos_1, noNeg_1, perPos_1, perNeg_1 = stat.stats1(reviews)
    noTotal_2, noPos_2, noNeg_2, perPos_2, perNeg_2 = stat.stats2(reviews)
    noTotal_3, noPos_3, noNeg_3, perPos_3, perNeg_3 = stat.stats3(reviews)
    
    perPos_1 = float("{:.2f}".format(perPos_1))
    perNeg_1 = float("{:.2f}".format(perNeg_1))
    perPos_2 = float("{:.2f}".format(perPos_2))
    perNeg_2 = float("{:.2f}".format(perNeg_2))
    perPos_3 = float("{:.2f}".format(perPos_3))
    perNeg_3 = float("{:.2f}".format(perNeg_3))
    
    sens = {
        'className': "Logistic Regression",
        'noTotal': noTotal_1,
        'noPos': noPos_1,
        'noNeg': noNeg_1, 
        'perPos': perPos_1,
        'perNeg': perNeg_1, 
    }
    
    sentiments['data'].append(sens)
    
    sens = {
        'className': "Stochastic Gradient Descent",
        'noTotal': noTotal_2,
        'noPos': noPos_2,
        'noNeg': noNeg_2, 
        'perPos': perPos_2,
        'perNeg': perNeg_2, 
    }
    
    sentiments['data'].append(sens)
    
    sens = {
        'className': "Multinomial NB",
        'noTotal': noTotal_3,
        'noPos': noPos_3,
        'noNeg': noNeg_3, 
        'perPos': perPos_3,
        'perNeg': perNeg_3, 
    }
    
    sentiments['data'].append(sens)
    
    with open('sentiments.json', 'w') as f:
        json.dump(sentiments, f)
    

def start_spider(spider, url):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('Scrapers')
    os.system('scrapy crawl ' + spider + ' -a url="' + url + '"')
    
def start_spider_without_url(spider):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('Scrapers')
    os.system("scrapy crawl " + spider)
    
def rev_collection(url):
    start_spider('rev_page_find', url)
    #time.sleep(6)
    start_spider_without_url('reviews')
    calc()
    
def create_product_list(url):
    start_spider('search_page_crawl', url)    