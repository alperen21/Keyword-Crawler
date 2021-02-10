from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.binary_location = '/Applications/Chrome.app/Contents/MacOS/Google Chrome'
# options.add_argument('headless')
options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(options=options)
driver.get('https://www.instagram.com')

time.sleep(3)
email = driver.find_element_by_xpath(
    "//*[@id='loginForm']/div/div[1]/div/label/input")

driver.close()
