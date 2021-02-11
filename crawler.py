from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json
from selenium.webdriver.firefox.options import Options
from EnvLoginGatherer import EnvLoginGatherer


class SponsorshipCrawler(EnvLoginGatherer):

    def __init__(self, json_directory="login.json", gecko_directory=r'/Users/alperen/Desktop/geckodriver', urls_directory="urls.json", sleep_for=3):
        # json_directory is the directory of the json file that contains the name of environment variables (see comments on EnvLoginGatherer.py )

        # gecko_directory is the directory that contains gecko driver

        # sleep_for is the length of time selenium will sleep between loading pages.
        # if its too long the execution will take a long time
        # if its too short selenium might try to grab an element before the page loads and then crash

        # urls directory is the directory which contains urls to visit for each social media website

        options = Options()
        options.add_argument('-headless')  # to toggle on headless option

        self.driver = webdriver.Firefox(
            executable_path=gecko_directory, options=options)  # this is the driver we will use throught the instance of the class
        self.sleep_for = sleep_for

        with open(urls_directory, "r") as f:  # loading urls to visit
            self.urls = json.load(f)

        super().__init__(json_directory)  # initialization for the parent class

    def execute_scroll_script(self):  # scrolls down
        scrolldown_script = "window.scrollTo(0, document.body.scrollHeight);"
        self.driver.execute_script(scrolldown_script)

    def instagram(self):
        # gathers information from instagram
        print("starting gathering information from instagram")
        self.driver.get('https://www.instagram.com')
        time.sleep(self.sleep_for)

        # finding the relevant elements
        email_input_area = self.driver.find_element_by_xpath(
            "//*[@id='loginForm']/div/div[1]/div/label/input")
        password_input_area = self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input')
        button = self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]/button')

        # getting email and password information from the parent class
        email = self.username("instagram")
        password = self.password("instagram")

        # logging in
        email_input_area.send_keys(email)
        password_input_area.send_keys(password)
        button.click()

        time.sleep(self.sleep_for)

        print("login successful")
        # visiting urls

        post = 'https://www.instagram.com/p/'
        with open("output.txt", "a") as f:

            for url in self.urls["instagram"]:  # for each account

                f.write(url + "\n\n")

                print("scraping: ", url)
                posts = []  # reset posts list
                self.driver.get(url)  # go to url page of the account
                time.sleep(self.sleep_for)
                count_outer = 0
                count_inner = 0
                iteration_number = 2  # How many times will the while loop iterate
                print("will find", iteration_number*2, "posts")

                while (len(posts) <= iteration_number*25):
                    count_outer += 1
                    links = [a.get_attribute(
                        'href') for a in self.driver.find_elements_by_tag_name('a')]

                    for link in links:
                        count_inner += 1
                        print("iteration", count_outer, ":", count_inner)
                        if post in link and link not in posts:
                            posts.append(link)
                    self.execute_scroll_script()
                    time.sleep(self.sleep_for)

                print("writing info on the txt file")
                for post_link in posts:
                    print("writing: ", post_link)
                    f.write(post_link + "\n")

    def close(self):
        self.driver.close()


crawler = SponsorshipCrawler()
crawler.instagram()
crawler.close()
