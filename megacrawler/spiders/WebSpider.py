import scrapy
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebSpider(scrapy.Spider):
    name = 'blogspider'
    global categories
    global count
    #categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'videogames']
    categories = ['tablets']
    #start_urls = ['https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn']
    #start_urls = ['http://www.bestbuy.com/site/searchpage.jsp?st='+
    #ategory
    #+'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys']

    def start_requests(self):
        urls = []
        """for category in categories:
            urls.append('http://www.bestbuy.com/site/searchpage.jsp?st='+
    category
    +'&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys')
        """
        urls = self.get_urls()
        for url in urls:
            global count
            count = 0
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        for title in response.css('div.fsdDeptCol'):
            yield {'title': title.css('a a-link-normal fsdLink fsdDeptLink::text').extract()}

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
"""
        for title in response.css('h4'):
            print "Inside title"
            yield {'title': title.css('a ::text').extract_first()}
            divs = response.css('div.list-item-postcard')
            for div in divs:
                yield {'properties': div.css('div.short-description li::text').extract()}
            '''
            for prop in response.css('div._MAj.shop__secondary'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}
            for propi in response.css('span._MAj'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}'''

        for next_page in response.css('li.pager-next > a'):
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
        driver.maximize_window()
        driver.get("https://www.bestbuy.com/")
        time.sleep(5)
        #print "In website"
        #driver.find_element_by_xpath("//*[@id='carousel_0']/div/div[1]/div/div").click()
        #time.sleep(10)
        urls=[]
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
            urls.append(driver.current_url)
        driver.quit()
        return urls


