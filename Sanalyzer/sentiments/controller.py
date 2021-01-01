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
    noTotal, noPos, noNeg, perPos, perNeg = stat.stats(reviews)
    
    perPos = float("{:.2f}".format(perPos))
    perNeg = float("{:.2f}".format(perNeg))
    
    sens = {
        'noTotal': noTotal,
        'noPos': noPos,
        'noNeg': noNeg, 
        'perPos': perPos,
        'perNeg': perNeg, 
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