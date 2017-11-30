import scrapy
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unicodedata
from pymongo import MongoClient

class WebSpider(scrapy.Spider):
    name = 'blogspider'
    global categories
    global count
    global current_key
    global urls
    categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'videogames']
    #categories = ['tablets']
    #start_urls = ['https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn']
    #start_urls = ['http://www.bestbuy.com/site/searchpage.jsp?st='+
    #ategory
    #+'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys']

    def start_requests(self):
        #urls = []
        """for category in categories:
            urls.append('http://www.bestbuy.com/site/searchpage.jsp?st='+
    category
    +'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys')
        """
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
        global current_key
        collection = self.getCollection()
        result = []
        '''
        for pb_price in response.css('div.pb.pb-price'):
            price = pb_price.css('span ::text').extract()[1]
            #print(1)
            print(title)
        '''
        for item in response.css('div.list-item'):
            #global current_key
            print "Inside title"
            #yield {'title': title.css('a ::text').extract_first()}
            #title = title.css('a ::text').extract_first()
            title = unicodedata.normalize('NFKD', item.css('h4 a ::text').extract_first()).encode('ascii', 'ignore')            
            price = unicodedata.normalize('NFKD', item.css('div.pb.pb-price span ::text').extract()[1]).encode('ascii', 'ignore')
            #divs = response.css('div.list-item-postcard')
            #for div in divs:
            #    yield {'properties': div.css('div.short-description li::text').extract()}
            if current_key == 'laptops':
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = title.split(' - ')
                print prop_list
                brand = prop_list[0]
                size = prop_list[1]
                processor = prop_list[2]
                ram = prop_list[3]
                storage = prop_list[-2]
                color = prop_list[-1]
                product_data = {
                    'product' : 'Laptop',
                    'brand': brand,
                    'price': price,
                    'size' : size,
                    'processor' : processor,
                    'ram' : ram,
                    'storage' : storage,
                    'color' : color
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if current_key == 'computers':
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = title.split(' - ')
                print prop_list
                brand = prop_list[0]
                name = prop_list[1]
                processor = prop_list[2]
                ram = prop_list[3]
                storage = prop_list[-2]
                color = prop_list[-1]
                product_data = {
                    'product' : 'Computer',
                    'brand': brand,
                    'price': price,
                    'size' : size,
                    'processor' : processor,
                    'ram' : ram,
                    'storage' : storage,
                    'color' : color
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if current_key == 'tablets':
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = title.split(' - ')                
                brand = prop_list[0]
                name = prop_list[1]
                size = prop_list[2]
                color = prop_list[-1]
                storage = prop_list[-2]
                '''
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
                        storage = item'''
                product_data = {
                    'product' : 'Tablet',
                    'brand' : brand,
                    'price' : price,
                    'name' : name,
                    'size' : size,
                    'color' : color,
                    'storage' : storage
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if current_key == 'cellphones':
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                prop_list = title.split(' - ')
                print prop_list
                brand = prop_list[0]
                name = prop_list[1]
                names = name.split(" ")
                color = prop_list[-1]
                for name in names:
                    if 'G' in name:
                        network = name
                    if 'GB' in name:
                        size = name
                product_data = {
                    'product' : 'Phone',
                    'brand' : brand,
                    'name' : name,
                    'price' : price,
                    'network' : network,
                    'size' : size
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if current_key == 'headphones':
                prop_list = title.split(' - ')
                brand = prop_list[0]
                name = prop_list[1]
                color = prop_list[-1]
                product_data = {
                    'brand': brand,
                    'name': name,
                    'price': price,
                    'color': color
                }
                print product_data

            if current_key == 'videogames':
                prop_list = title.split(' - ')
                brand = prop_list[0]
                name = prop_list[-1]
                product_data = {
                    'brand': brand,
                    'name': name,
                    'price': price
                }
                print product_data

            result.append(product_data)

        for next_page in response.css('li.pager-next > a'):
            global count
            count += 1
            print "\n \n \n \n \n \n \n \n \n \n \n \n next page " + str(count)
            if count > 3:
                break
            yield response.follow(next_page, self.parse)
            #div._MAj.shop__secondary
        collection.insert_many(result)
    
    def get_urls(self):
        driver = webdriver.Firefox()
        #driver.set_window_size(1120, 550)
        driver.maximize_window()
        driver.get("https://www.bestbuy.com/")
        time.sleep(5)
        #print "In website"
        #driver.find_element_by_xpath("//*[@id='carousel_0']/div/div[1]/div/div").click()
        #time.sleep(10)
        urls={}
        for category in categories:
            time.sleep(5)
            element = driver.find_element_by_id("gh-search-input")
            element.clear()
            element.send_keys(category + " in all")
            element.submit()
            #driver.find_element_by_id("gbqfb").click()
            time.sleep(5)
            print "These are the urls you want"
            print driver.current_url
            urls[category]=driver.current_url
        driver.quit()
        return urls

    def getCollection(self):
        client = MongoClient('ds227865.mlab.com', 27865)
        db = client.productdb
        db.authenticate('admin', 'admin')
        collection = db.product_collection
        return collection

