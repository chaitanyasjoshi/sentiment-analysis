'''
Created on 23-Nov-2020

@author: Chaitanya Joshi
'''


import scrapy
from scrapy.crawler import CrawlerProcess
import json
import pandas as pd
import os

data = {}

class IndividualRevSpider(scrapy.Spider):
    name = "indi_rev"
    
    urls = []
    #reviews = []
    #revs = {}
    custom_settings = {
        #'DOWNLOAD_DELAY': 0.5,
        'DOWNLOAD_TIMEOUT': 10,
        'AUTOTHROTTLE_ENABLED': False,
        'USER_AGENT': 'Mediapartners-Google/2.1',
        'ROBOTSTXT_OBEY' : True,
        'CONCURRENT_REQUESTS' : 500,
        'REACTOR_THREADPOOL_MAXSIZE' : 500,
        'CONCURRENT_ITEMS': 500,
        'SCHEDULER_PRIORITY_QUEUE' : 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'COOKIES_ENABLED' : False,
        #'SPIDER_MIDDLEWARES' : {
         #   'Scrapers.middlewares.ScrapersSpiderMiddleware': 543,
        #},
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'Scrapers.middlewares.ScrapersDownloaderMiddleware': 543,
        #}
    }
    
    def start_requests(self):
        self.urls = self.webpages
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_rev)
        
        #self.revs = {
        #    'reviews': self.reviews,
        #}
        #with open("../reviews.json", "w") as outfile:  
        #    json.dump(self.revs, outfile) 
            
    def parse_rev(self, response):
        divs = response.xpath("//*[contains(@class, 't-ZTKy')]")
        rev = []
        for div in divs:
            rev.append(str(div.xpath('div/div/text()').get()))
            #print(str(div.xpath('div/div/text()').get()))
        
        data = pd.DataFrame({'Reviews': rev})
        with open('reviews.csv', 'a', encoding='utf-8', newline="") as f:
            data.to_csv(f, sep = ',', header=False, index=False)  
        #self.reviews.append(rev)
        

class ReviewSpider(scrapy.Spider):
    name = "reviews"
    
    urls = ''
    webpages = []
    
    allowed_domains = [
        'flipkart.com',
    ]
    
    custom_settings = {
        #'DOWNLOAD_DELAY': 0.5,
        'DOWNLOAD_TIMEOUT': 10,
        'AUTOTHROTTLE_ENABLED': False,
        'USER_AGENT': 'Mediapartners-Google/2.1',
        'ROBOTSTXT_OBEY' : True,
        'CONCURRENT_REQUESTS' : 500,
        'REACTOR_THREADPOOL_MAXSIZE' : 500,
        'CONCURRENT_ITEMS': 500,
        'SCHEDULER_PRIORITY_QUEUE' : 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'COOKIES_ENABLED' : False,
        #'SPIDER_MIDDLEWARES' : {
         #   'Scrapers.middlewares.ScrapersSpiderMiddleware': 543,
        #},
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'Scrapers.middlewares.ScrapersDownloaderMiddleware': 543,
        #}
    }
    
    def start_requests(self):
        with open('review_url.txt', 'r') as f:
            self.urls = str(f.read())
        yield scrapy.Request(url=self.urls, callback=self.find_pages)
        
    def find_pages(self, response):
        if os.path.exists("reviews.csv"):
            os.remove("reviews.csv")
            
        req = str(response.xpath('//*[@id="container"]/div/div[3]/div/div/div[2]/div[13]/div/div/span[1]/text()').get()).split(" ")[-1]
        if req == 'None':
            print("##################")
            self.webpages.append(self.urls)
        else:
            text = int(req) + 1
            print("Pages: " + str(text))
            for i in range(1, (text+1)):
                self.webpages.append(self.urls + '&page=' + str(i))
         
         
        #print(len(self.webpages))   
        process = CrawlerProcess()
        process.crawl(IndividualRevSpider, webpages=self.webpages)
        process.start() 
        
        
'''
Created on 25-Nov-2020

@author: Chaitanya Joshi
'''
        
class ReviewPageFinder(scrapy.Spider):
    name = 'rev_page_find'
    
    urls = ''
    
    base_url = 'https://www.flipkart.com'
    
    allowed_domains = [
        'flipkart.com',
    ]
    
    custom_settings = {
        #'DOWNLOAD_DELAY': 0.5,
        'AUTOTHROTTLE_ENABLED': False,
        'USER_AGENT': 'Mediapartners-Google/2.1',
        'ROBOTSTXT_OBEY' : True,
        'CONCURRENT_REQUESTS' : 500,
        'REACTOR_THREADPOOL_MAXSIZE' : 500,
        'CONCURRENT_ITEMS': 500,
        'SCHEDULER_PRIORITY_QUEUE' : 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'COOKIES_ENABLED' : False,
        #'SPIDER_MIDDLEWARES' : {
         #   'Scrapers.middlewares.ScrapersSpiderMiddleware': 543,
        #},
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'Scrapers.middlewares.ScrapersDownloaderMiddleware': 543,
        #}
    }
    
    def start_requests(self):
        self.urls = self.base_url + self.url
        yield scrapy.Request(url=self.urls, callback=self.find_rev)
        
    def find_rev(self, response):
        if os.path.exists('review_url.txt'):
            os.remove('review_url.txt')
        
        new_url = response.xpath('//*[contains(@class, "col JOpGWq")]/a/@href').get()
        
        if new_url == 'None':
            with open('error.log', 'w') as file:
                file.write("ERROR No element")
                
        else:
            #new_url = str(new_url).replace('&marketplace=FLIPKART', '')
            
            with open('review_url.txt', 'w') as f:
                f.write(str(self.base_url + new_url))
                f.close() 
            #process = CrawlerProcess()
            #process.crawl(ReviewSpider, url=str(self.base_url + new_url))
            #process.start() 

class SearchPageCrawler(scrapy.Spider):
    name = "search_page_crawl"
    
    urls = ''
    
    allowed_domains = [
        'flipkart.com',
    ]
    
    PAGE_LIMIT = 10
    CUR_PAGE = 1
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 10,
        'AUTOTHROTTLE_ENABLED': False,
        'USER_AGENT': 'Mediapartners-Google/2.1',
        'ROBOTSTXT_OBEY' : True,
        'CONCURRENT_REQUESTS' : 500,
        'REACTOR_THREADPOOL_MAXSIZE' : 500,
        'CONCURRENT_ITEMS': 500,
        'SCHEDULER_PRIORITY_QUEUE' : 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'COOKIES_ENABLED' : False,
        #'SPIDER_MIDDLEWARES' : {
         #   'Scrapers.middlewares.ScrapersSpiderMiddleware': 543,
        #},
        #'DOWNLOADER_MIDDLEWARES' : {
        #    'Scrapers.middlewares.ScrapersDownloaderMiddleware': 543,
        #}
    }
    
    def start_requests(self):
        self.urls = self.url
        if os.path.exists("products.json"):
            os.remove("products.json")
        data = {}
        data['data'] = []
        with open('products.json', 'w+') as f:
            json.dump(data, f)
            f.close()
        yield scrapy.Request(url=self.urls, callback=self.parse_all)
        
    def parse_all(self, response):
        product_info = {}
        main_div = response.xpath('//*[@id="container"]/div/div[3]/div[2]/div[1]/div[2]')
        row_divs = main_div.xpath("*[contains(@class, '_2pi5LC col-12-12')]")
        print("#######" + str(len(row_divs)))
        for row in row_divs[:-2]:
            prod_link = row.xpath('div/div/div/a/@href').get()
            prod_name = row.xpath('div/div/div/a/div[2]/div[1]/div[1]/text()').get()
            prod_price = row.xpath('div/div/div/a/div[2]/div[2]/div[1]/div/div/text()').get()
            prod_ratings = str(row.xpath('div/div/div/a/div[2]/div[1]/div[2]/span[2]/span/span[1]/text()').get()).split(" ")[0]
            prod_reviews = str(row.xpath('div/div/div/a/div[2]/div[1]/div[2]/span[2]/span/span[3]/text()').get()).split(" ")[0][1:]
            prod_stars = str(row.xpath('div/div/div/a/div[2]/div[1]/div[2]/span[1]/div/text()').get())
            
            if prod_link == 'None':
                continue
            if prod_name is None:
                continue
            if prod_price is None:
                continue
            if prod_ratings == 'None':
                continue
            if prod_stars == 'None':
                continue
            if prod_reviews == 'one':
                continue
            if int(''.join(prod_reviews.split(','))) < 5:
                sentible = 0
            else:
                sentible = 1
            product_info = {
                'link' : prod_link,
                'name' : prod_name,
                'price' : prod_price,
                'ratings' : prod_ratings,
                'reviews' : prod_reviews,
                'stars' : prod_stars,
                'sentible': sentible, 
            }
            
            dic = {}
            
            with open('products.json','r') as f: 
                dic = json.load(f)
                f.close()
                
            dic['data'].append(product_info)
            
            with open('products.json', 'w') as f:
                json.dump(dic, f, indent=4)
                
        pages = int(row_divs[-2].xpath('div/div/span[1]/text()').get().split(" ")[-1])
        print("Pages: " + str(pages))
        
        if self.CUR_PAGE < min(self.PAGE_LIMIT, pages):
            self.CUR_PAGE += 1
            new_url = self.urls + "&page=" + str(self.CUR_PAGE)
            yield response.follow(new_url, self.parse_all)
        