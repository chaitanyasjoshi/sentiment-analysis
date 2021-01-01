from django.shortcuts import render
from Sanalyzer.sentiments.controller import create_product_list, rev_collection
import json
import os
from django.http import JsonResponse

# Create your views here.
def search(request, search=None):
    if search == None:
        return render(request, 'Home.html', {})
    
    url = 'http://www.flipkart.com/search?q=' + search
    create_product_list(url)
    return render(request, 'Home.html', {})


def request_products(request):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '\\sentiments\\Scrapers\\products.json') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)

def find_reviews(request, index=None):
    if index == None:
        return render(request, 'Home.html', {})
    
    link = ''
    count = 0
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '\\sentiments\\Scrapers\\products.json') as f:
        dic = json.load(f)
        for i in dic['data']:
            if count == int(index):
                link = i['link']
            count += 1
        f.close() 
                
    rev_collection(link)
    return render(request, 'Home.html', {})

def request_sentiments(request):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '\\sentiments\\Scrapers\\sentiments.json') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)