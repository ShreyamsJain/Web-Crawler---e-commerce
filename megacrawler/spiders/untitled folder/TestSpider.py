import scrapy
import pymongo
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time

class WebSpider(scrapy.Spider):
    name = 'newblogspider'
    global categories
    global count
    categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'homeaudio', 'tv', 'videogames']
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
        #urls = self.get_urls()
        urls = ['https://www.google.com/search?output=search&tbm=shop&q=samsung+galaxy+s8&source=pshome-c-0-0&sa=X&ved=0ahUKEwja7bHLtq3WAhWHs1QKHXpAB5UQ7j8IBw']
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
        for title in response.css('h3.r'):
            print "Inside title"
            yield {'title': title.css('a ::text').extract_first()}
            for prop in response.css('div._MAj.shop__secondary'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}
            for propi in response.css('span._MAj'):
                print "inside span"
                yield {'property': prop.css('span ::text').extract_first()}

        for next_page in response.css('td > a.fl'):
            global count
            count += 1
            print "next page " + str(count)
            if count > 3:
                break
            yield response.follow(next_page, self.parse)