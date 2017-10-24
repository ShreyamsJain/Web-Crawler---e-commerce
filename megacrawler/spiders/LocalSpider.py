import scrapy
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unicodedata
from pymongo import MongoClient


class ComSpider(scrapy.Spider):
    name = 'blogspider'
    global categories
    global count
    global urls
    global current_key
    #categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'videogames']
    categories = ['tablets']
    #start_urls = ['https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn']
    #start_urls = ['http://www.bestbuy.com/site/searchpage.jsp?st='+
    #ategory
    #+'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys']
    #client = MongoClient('localhost', 27017)
    #db = client.mydb

    def start_requests(self):
        #urls = {}
        """for category in categories:
            urls.append('http://www.bestbuy.com/site/searchpage.jsp?st='+
    category
    +'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys')
        """
        global urls
        global current_key
        urls = self.get_urls()
        for key, url in urls.iteritems():
            global count
            global current_key
            current_key = key
            count = 0
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        for title in response.css('div.fsdDeptCol'):
            yield {'title': title.css('a a-link-normal fsdLink fsdDeptLink::text').extract()}

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
"""
        collection = self.getCollection()
        global current_key
        '''
        for divcap in response.css('div.caption'):
            yield {'title': divcap.css('a.title ::text').extract_first()}
            yield {'price': divcap.css('h4.pull-right.price ::text').extract_first()}
            yield {'Description': divcap.css('p.description ::text').extract_first()}
        '''
        for divcap in response.css('div.caption'):
            if current_key == 'Laptops':
                title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = properties.split(',')
                size = prop_list[0]
                processor = prop_list[1]
                ram = prop_list[2]
                storage = prop_list[3]
                os = prop_list[4]
                product_data = {
                    'product' : 'Laptop',
                    'title': title,
                    'price': price,
                    'size' : size,
                    'processor' : processor,
                    'ram' : ram,
                    'storage' : storage,
                    'os' : os
                }
                result = collection.insert_one(product_data)
                print('One post: {0}'.format(result.inserted_id))

            if current_key == 'Tablets':
                title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = properties.split(',')                
                size = ''
                os = ''
                processor = ''
                color = ''
                storage = ''
                for item in prop_list:
                    if '"' in item: 
                        size = item
                    if 'Android' in item:
                        os = item
                    if 'GHz' in item:
                        processor = item
                    if 'Black' in item or 'White' in item:
                        color = item
                    if 'GB' in item:
                        storage = item
                product_data = {
                    'product' : 'Tablet',
                    'title' : title,
                    'price' : price,
                    'size' : size,
                    'os' : os,
                    'processor' : processor,
                    'color' : color,
                    'storage' : storage
                }
                result = collection.insert_one(product_data)
                print('One post: {0}'.format(result.inserted_id))

            if current_key == 'Phones':
                title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = properties.split(',')
                os = ''
                size = ''
                for item in prop_list:
                    if 'Android' in item:
                        os = item
                    if '"' in item:
                        size = item
                product_data = {
                    'product' : 'Phone',
                    'title' : title,
                    'price' : price,
                    'os' : os,
                    'size' : size
                }
                result = collection.insert_one(product_data)
                print('One post: {0}'.format(result.inserted_id))
            '''
            yield {'title': divcap.css('a.title ::text').extract_first()}
            yield {'price': divcap.css('h4.pull-right.price ::text').extract_first()}
            yield {'Description': divcap.css('p.description ::text').extract_first()}
            
            divs = response.css('div.list-item-postcard')
            for div in divs:
                yield {'properties': div.css('div.short-description li::text').extract()}
            
            for prop in response.css('div._MAj.shop__secondary'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}
            for propi in response.css('span._MAj'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}'''

        for next_page in response.css('ul.pagination > li > a'):
            global count
            count += 1
            print "\n \n \n \n \n \n \n \n \n \n \n \n next page " + str(count)
            if count > 3:
                break
            yield response.follow(next_page, self.parse)
            #div._MAj.shop__secondary
    def get_urls(self):
        driver = webdriver.Firefox()
        #driver.set_window_size(1120, 550)
        urls = {}
        driver.maximize_window()
        driver.get("http://webscraper.io/test-sites/e-commerce/static")
        time.sleep(5)
        #print "In website"
        #driver.find_element_by_xpath("//*[@id='carousel_0']/div/div[1]/div/div").click()
        #time.sleep(10)
        driver.find_element_by_xpath('//*[@id="side-menu"]/li[2]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="side-menu"]/li[2]/ul/li[1]/a').click()
        time.sleep(3)
        urls['Laptops'] = driver.current_url
        driver.find_element_by_xpath('//*[@id="side-menu"]/li[2]/ul/li[2]/a').click()
        time.sleep(3)
        urls['Tablets'] = driver.current_url
        driver.find_element_by_xpath('//*[@id="side-menu"]/li[3]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="side-menu"]/li[3]/ul/li/a').click()
        time.sleep(3)
        urls['Phones'] = driver.current_url
        driver.quit()
        return urls

    def getCollection(self):
        client = MongoClient('localhost', 27017)
        db = client.mydb
        collection = db.products
        return collection

