from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('-headless')

driver = webdriver.Firefox(
    executable_path=r'/Users/alperen/Desktop/geckodriver', options=options)
driver.get('https://www.instagram.com')

time.sleep(3)
email = driver.find_element_by_xpath(
    "//*[@id='loginForm']/div/div[1]/div/label/input")

driver.close()
