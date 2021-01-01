'''
Created on 21-Nov-2020

@author: Chaitanya Joshi
'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from Sanalyzer.sentiments import statistics as st
import time
import concurrent.futures

def revscrap(url):
    #params = []
    rev = []
    time.sleep(0.5)
    req = Request(url, headers={'User-Agent': 'Mediapartners-Google/2.1'})
    response = urlopen(req).read()
    soup = bs(response, "html.parser")
    subrevs = soup.findAll("div", attrs={"class", "t-ZTKy"})
    for j in range(len(subrevs)):
        rev.append(subrevs[j].text)
    
    return rev
    
def parseMult(url):
    req = Request(url, headers={'User-Agent': 'Mediapartners-Google/2.1'})
    response = urlopen(req).read()
    soup = bs(response, "html.parser")
    subrevs = soup.findAll("div", attrs={"class", "_2MImiq _1Qnn1K"})
    subrevs = subrevs[0].findChildren("span", recursive=False)
    page_limit = int(str(subrevs[0].text).split(" ")[-1])
    print(str(page_limit))
    reviews = []
    websites = []
    #params = []
    for i in range (1, page_limit):
        websites.append(url + "&page="+ str(i))
        
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(revscrap, u) for u in websites]
        reviews.append([f.result() for f in futures])
        
    noTotal, noPos, noNeut, noNeg, perPos, perNeut, perNeg = st.stats(reviews)
    
    print("noTotal: " + str(noTotal))
    print("noPos: " + str(noPos))
    print("noNeut: " + str(noNeut))
    print("noNeg: " + str(noNeg))
    print("perPos: " + str(perPos))
    print("perNeut: " + str(perNeut))
    print("perNeg: " + str(perNeg))
        
parseMult("https://www.flipkart.com/apple-macbook-air-core-i5-5th-gen-8-gb-128-gb-ssd-mac-os-sierra-mqd32hn-a-a1466/product-reviews/itmevcpqqhf6azn3?pid=COMEVCPQBXBDFJ8C" )