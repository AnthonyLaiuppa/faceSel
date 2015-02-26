#! Usr/bin/env python   

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from parser import Parser 
import time


def main():

    #Basic Biz to log into facebook and navigate to albums
    driver = webdriver.Firefox()
    driver.get("http://www.facebook.com/login.php")
    element = driver.find_element_by_name("email")
    element.send_keys("username")
    element = driver.find_element_by_name("pass")
    element.send_keys("pass");
    element = driver.find_element_by_id("loginbutton").click()
    url = "http://www.facebook.com/username/photos_albums"
    driver.get(url)
    time.sleep(5)
    
    #Something is going to scrape the source
    #response = driver.page_source #-- Didnt work:(
    #response = BeautifulSoup(url.read()) -- Didnt work:(
    #Lines 28 and 29 actually scrape it!!!!!
    response=driver.page_source.encode('utf-8')
    html_str=str(response)
    
    #Pull the source down into a text file once we bypass the JS
    target = open("testing.txt", "w")
    target.write(html_str)
    target.close()

    #Send it to the parser class to sort out albums
    parser = Parser()
    parser.set_soup(html_str)
    albums = parser.get_album_links()

    #print(albums) -- Works up to this point

    for a in albums #<---- Problem statement
        driver.get(albums["url"])
        response=driver.page_source.encoude('utf-8')
        html_str = str(response)
        parser.set_soup(html_str)
        pictures = parser.get_picture_links()

    #print(pictures)



    driver.close()

if __name__ == '__main__': main()