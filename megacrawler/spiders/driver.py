'''
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

categories = ['tablets', 'computers', 'laptops', 'cellphones', 'headphones', 'homeaudio', 'tv', 'videogames']
#driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver = webdriver.Firefox()
driver.set_window_size(1120, 550)
#driver.maximize_window()
driver.get("https://www.google.com/shopping")
print "Inside Website"
time.sleep(5)
#driver.save_screenshot('/Users/Shreyams/Desktop/out.png');
#driver.find_element_by_xpath("//*[@id='carousel_0']/div/div[1]/div/div").click()
#driver.find_element_by_class_name("_guc").click()
driver.find_element_by_link_text("Sunscreen").click()
#driver.find_element_by_css_selector("#carousel_0 > div > div:nth-child(1) > div > div > a").click()
print "Clicked item"
for category in categories:
    #driver.set_window_size(1120, 550)
    print "Inside loop waiting...."
    time.sleep(5)
#element = driver.find_element_by_id("lst-ib")
    #element = driver.find_element_by_class_name("gsfi")
    #element = driver.find_element_by_css_selector("#lst-ib > input")
    element = driver.find_element_by_xpath("//*[@id='lst-ib']")
    print "Found element"
    element.clear()
    print "Cleared search field"
    element.send_keys(category)
    print "Keys sent"
    element.submit()
    print "clicked enter"
#driver.find_element_by_id("gbqfb").click()
    time.sleep(5)
    print "These are the urls you want"
    print driver.current_url
driver.quit()
"""https://www.google.com/search?q=tablets&source=lnms&tbm=shop&sa=X&ved=0ahUKEwi3yd-EyozWAhUqjlQKHfVAAdsQ_AUICigB&biw=1280&bih=698"""
'''