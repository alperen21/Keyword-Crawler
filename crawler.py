from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from EnvLoginGatherer import EnvLoginGatherer


class SponsorshipCrawler(EnvLoginGatherer):

    def __init__(self, json_directory="login.json", gecko_directory=r'/Users/alperen/Desktop/geckodriver'):
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(
            executable_path=gecko_directory, options=options)
        super().__init__(json_directory)

    def instagram(self):
        self.driver.get('https://www.instagram.com')
        time.sleep(3)
        email = self.driver.find_element_by_xpath(
            "//*[@id='loginForm']/div/div[1]/div/label/input")

    def close(self):
        self.driver.close()


crawler = SponsorshipCrawler()
crawler.instagram()
crawler.close()
