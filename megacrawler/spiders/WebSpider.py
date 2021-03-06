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
    global result
    result = []
    categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'videogames']
    #categories = ['tablets']
    #start_urls = ['https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn']
    #start_urls = ['http://www.bestbuy.com/site/searchpage.jsp?st='+
    #ategory
    #+'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys']

    #def __init__(self):
    #    self.result = []

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
            print "current key is ------------------------------>" + current_key
            count = 0
            yield scrapy.Request(url=url, callback=self.parse, meta={'item': current_key})

        yield scrapy.Request(url="http://www.google.com", callback=self.parseData)
        print "End----------------------------------------------->"

    def parse(self, response):
        """
        for title in response.css('div.fsdDeptCol'):
            yield {'title': title.css('a a-link-normal fsdLink fsdDeptLink::text').extract()}

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
"""
        global current_key
        #global result
        key = response.meta['item']
        print "Key is --------------------------------------------->>>>>" + str(key)
        collection = self.getLocalCollection()
        #result = []
        '''
        for pb_price in response.css('div.pb.pb-price'):
            price = pb_price.css('span ::text').extract()[1]
            #print(1)
            print(title)
        '''
        for item in response.css('div.list-item'):
            #global current_key
            print "Inside title"
            print current_key
            #global result
            #yield {'title': title.css('a ::text').extract_first()}
            #title = title.css('a ::text').extract_first()
            title = unicodedata.normalize('NFKD', item.css('h4 a ::text').extract_first()).encode('ascii', 'ignore')            
            price = unicodedata.normalize('NFKD', item.css('div.pb.pb-price span ::text').extract()[1]).encode('ascii', 'ignore')
            image_url = unicodedata.normalize('NFKD', item.css('div.thumb ::attr(src)').extract_first()).encode('ascii', 'ignore')
            img_url, sep, tail = image_url.partition(';')
            product_url = unicodedata.normalize('NFKD', item.css('h4 a ::attr(href)').extract_first()).encode('ascii', 'ignore')
            pro_url = "http://www.bestbuy.com" + product_url
            prop_list = title.split(' - ')
            for index, feature in enumerate(prop_list):
                prop_list[index] = feature.replace(" ", "_")
            #divs = response.css('div.list-item-postcard')
            #for div in divs:
            #    yield {'properties': div.css('div.short-description li::text').extract()}
            if key == 'laptops':
                print "Inside Laptops"
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                #prop_list = title.split(' - ')
                size, storage, processor, ram = '','','',''
                print prop_list
                brand = prop_list[0]
                if len(prop_list)>1:
                    size = prop_list[1]
                    storage = prop_list[-2]
                if len(prop_list)>2:
                    processor = prop_list[2]
                if len(prop_list)>3:
                    ram = prop_list[3]
                color = prop_list[-1]
                product_data = {
                    'product' : 'Laptop',
                    'brand': brand,
                    'price': price,
                    'size' : size,
                    'processor' : processor,
                    'ram' : ram,
                    'storage' : storage,
                    'color' : color,
                    'img_url' : img_url,
                    'pro_url' : pro_url
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if key == 'computers':
                print "Inside Computer"
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                #prop_list = title.split(' - ')
                print prop_list
                name, storage, processor, ram = '','','',''
                brand = prop_list[0]
                if len(prop_list)>1:
                    name = prop_list[1]
                    storage = prop_list[-2]
                if len(prop_list)>2:
                    processor = prop_list[2]
                if len(prop_list)>3:
                    ram = prop_list[3]
                color = prop_list[-1]
                product_data = {
                    'product' : 'Computer',
                    'brand': brand,
                    'price': price,
                    'processor' : processor,
                    'ram' : ram,
                    'storage' : storage,
                    'color' : color,
                    'img_url' : img_url,
                    'pro_url' : pro_url
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if key == 'tablets':
                print "Inside tablets"
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                #prop_list = title.split(' - ')                
                brand = prop_list[0]
                name, size, storage = '','',''
                if len(prop_list)>1:
                    name = prop_list[1]
                if len(prop_list)>2:
                    size = prop_list[2]
                    storage = prop_list[-2]
                color = prop_list[-1]
                
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
                    'storage' : storage,
                    'img_url' : img_url,
                    'pro_url' : pro_url
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if key == 'cellphones':
                print "Inside cellphones"
                #title = unicodedata.normalize('NFKD', divcap.css('a.title ::text').extract_first()).encode('ascii', 'ignore')
                #price = unicodedata.normalize('NFKD', divcap.css('h4.pull-right.price ::text').extract_first()).encode('ascii', 'ignore')
                #properties = unicodedata.normalize('NFKD', divcap.css('p.description ::text').extract_first()).encode('ascii', 'ignore')
                #prop_list = title.split(' - ')
                print prop_list
                name, network, size = '','',''
                brand = prop_list[0]
                if len(prop_list)>1:
                    name = prop_list[1]
                names = name.split("_")
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
                    'size' : size,
                    'img_url' : img_url,
                    'pro_url' : pro_url
                }
                print product_data
                #result = collection.insert_one(product_data)
                #print('One post: {0}'.format(result.inserted_id))

            if key == 'headphones':
                print "Inside headphones"
                #prop_list = title.split(' - ')
                brand = prop_list[0]
                name = ''
                if len(prop_list)>1:
                    name = prop_list[1]
                color = prop_list[-1]
                product_data = {
                    'product' : 'Headphones',
                    'brand': brand,
                    'name': name,
                    'price': price,
                    'color': color,
                    'img_url' : img_url,
                    'pro_url' : pro_url
                }
                print product_data

            if key == 'videogames':
                print "Inside videogames"
                #prop_list = title.split(' - ')
                brand = prop_list[0]
                name = prop_list[-1]
                product_data = {
                    'product': 'Videogames',
                    'brand': brand,
                    'name': name,
                    'price': price,
                    'img_url': img_url,
                    'pro_url': pro_url
                }
                print product_data

            result.append(product_data)

        for next_page in response.css('li.pager-next > a'):
            global count
            count += 1
            print "\n \n \n \n \n \n \n \n \n \n \n \n next page " + str(count)
            if count > 5:
                break
            yield response.follow(next_page, self.parse, meta={'item':key})
            #div._MAj.shop__secondary
        
        result_dict = {'Bestbuy' : result}
        collection.insert_one(result_dict)

    def parseData(self, response):
        #global result
        collection_local = self.getLocalCollection()
        res = collection_local.distinct('Bestbuy')
        '''
        for document in collection_local.find():
            for item in document['Bestbuy']:
                res.append(item)'''
        result_dict = {'Best Buy': res}
        collection = self.getCollection()
        collection.insert_one(result_dict)

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

    def getLocalCollection(self):
        client = MongoClient('localhost', 27017)
        db = client.mydb
        collection = db.product_col
        return collection