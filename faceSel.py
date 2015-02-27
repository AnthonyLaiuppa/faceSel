""" this is a docstring """
#from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
from parser import Parser
import time, os, simplejson
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def main():
    """
        this is the main method
    """

    """
    #Basic Biz to log into facebook and navigate to albums
    chromedriver = "/home/mowens/Desktop/facebook/chromedriver"
    os.environ['webdriver.chrome.driver'] = chromedriver

    #driver = webdriver.Remote(command_executor='http://10.8.0.1:4444/wd/hub',
    #    desired_capabilities=DesiredCapabilities.CHROME)

    driver = webdriver.Chrome(chromedriver)
    """

    driver = webdriver.Firefox()
    driver.get("http://www.facebook.com/login.php")

    element = driver.find_element_by_name("email")
    element.send_keys("")
    element = driver.find_element_by_name("pass")
    element.send_keys("")
    element = driver.find_element_by_id("loginbutton").click()

    url = "http://www.facebook.com/username/photos_albums"

    driver.get(url)
    time.sleep(5)

    response = driver.page_source.encode('utf-8')
    html_str = str(response)

    #Send it to the parser class to sort out albums
    parser = Parser()
    parser.set_soup(html_str)
    albums = parser.get_album_links()

    for key, album in albums.items():
        driver.get(album["url"])
        response = driver.page_source.encode('utf-8')
        html_str = str(response)
        parser.set_soup(html_str)
        pictures = parser.get_picture_links(key)

    url = "http://www.facebook.com/username/photos_of"
    driver.get(url)
    time.sleep(5)


    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            element = driver.find_element_by_class_name("sectionHeader")
            break
        except:
            continue

    response = driver.page_source.encode('utf-8')
    parser = Parser()
    parser.set_soup(html_str)
    parser.get_picture_links('tagged')

    parser.create_files()
    target = open("results.txt", "w")
    target.write(parser.get_data_json())
    target.close()

if __name__ == '__main__':
    main()
