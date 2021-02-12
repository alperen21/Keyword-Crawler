#!/usr/bin/python3
from selenium import webdriver
import time
import json
from selenium.webdriver.firefox.options import Options
from EnvLoginGatherer import EnvLoginGatherer
import sys
import re


class KeywordCrawler(EnvLoginGatherer):

    def __init__(self, gecko_directory, login_directory="login.json", search_directory="search.json", sleep_for=3, depth=2, url_only=True):
        # login_directory is the directory of the json file that contains the name of environment variables (see comments on EnvLoginGatherer.py )

        # gecko_directory is the directory that contains gecko driver

        # sleep_for is the length of time selenium will sleep between loading pages.
        # if its too long the execution will take a long time
        # if its too short selenium might try to grab an element before the page loads and then crash

        # search directory is the directory which contains urls to visit for each social media website and the keywords

        # depth levels are how deep down the posts will the crawler go

        # if url only is set to true, the script will not write down the contents of the findings, just urls

        options = Options()
        options.add_argument('-headless')  # to toggle on headless option

        self.driver = webdriver.Firefox(
            executable_path=gecko_directory, options=options)  # this is the driver we will use throught the instance of the class
        self.sleep_for = sleep_for
        self.depth = depth

        try:  # try except blocks are there for more meaningful errors rather than generic errors
            with open(search_directory, "r") as f:  # loading urls to visit
                json_data = json.load(f)
        except:
            print("can't find search.json")
            sys.exit()

        try:
            self.urls = json_data['urls']
        except:
            print("cannot find urls in search.json")
            sys.exit()

        try:
            self.keywords = json_data['keywords']
        except:
            print("cannot find keywords in search.json")
            sys.exit()

        print("search.json has been parsed successfully")
        self.url_only = url_only
        super().__init__(login_directory)  # initialization for the parent class

    def execute_scroll_script(self):  # scrolls down
        scrolldown_script = "window.scrollTo(0, document.body.scrollHeight);"
        self.driver.execute_script(scrolldown_script)

    def instagram_login(self):
        # gathers information from instagram
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

        print("logged in to instagram as:", email)

    def instagram(self):
        # logging in
        self.instagram_login()

        # visiting urls
        post = 'https://www.instagram.com/p/'
        with open("output.txt", "a") as f:

            for url in self.urls["instagram"]:  # for each account

                f.write("#information found for: " + url + "\n\n")

                print("scraping: ", url)
                posts = []  # reset posts list
                self.driver.get(url)  # go to url page of the account
                time.sleep(self.sleep_for)
                print("will find approx.", self.depth*30, "posts")

                while (len(posts) <= self.depth*25):
                    links = [a.get_attribute(
                        'href') for a in self.driver.find_elements_by_tag_name('a')]

                    for link in links:
                        if post in link and link not in posts:
                            posts.append(link)
                    self.execute_scroll_script()
                    time.sleep(self.sleep_for)

                for post_link in posts:
                    self.search_instagram(f, post_link)

    def get_instagram_text(self, url):
        # in: instagram post url
        # out: text of the instagram post

        self.driver.get(url)
        time.sleep(self.sleep_for)
        text = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text

        return text.lower()

    def search_instagram(self, f, url):
        text = self.get_instagram_text(url)
        for word in self.keywords:
            if re.search("(?<![\w\d])"+word+"(?![\w\d])", text):

                if (self.url_only):
                    f.write(url + "\n")
                    return
                else:
                    f.write(text + "\n" + "source: " + url + "\n")
                    print("a post containing the key word found")
                    return

    def twitter_login(self):

        # sending request
        self.driver.get('https://twitter.com/login')
        time.sleep(self.sleep_for)

        # locating relevant elements
        username_input = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        password_input = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        button = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div')

        # gathering username and password information
        email = self.username("twitter")
        password = self.password("twitter")

        # logging in
        username_input.send_keys(email)
        password_input.send_keys(password)
        button.click()

        time.sleep(self.sleep_for)
        print("logged in to twitter as:", email)

    def twitter(self):
        self.twitter_login()
        with open("output.txt", "a") as f:

            for url in self.urls["twitter"]:  # for each account
                post = url + "/status/"
                f.write("#information found for: " + url + "\n\n")

                print("scraping: ", url)
                posts = []  # reset posts list
                self.driver.get(url)  # go to url page of the account
                time.sleep(self.sleep_for)
                print("will find approx.", self.depth*25, "posts")

                while (len(posts) <= self.depth*25):
                    links = [a.get_attribute(
                        'href') for a in self.driver.find_elements_by_tag_name('a')]
                    for link in links:
                        if post in link and link not in posts:

                            posts.append(link)
                    self.execute_scroll_script()
                    time.sleep(self.sleep_for)

                for post_link in posts:
                    if "/photo" not in post_link and "/media_tags" not in post_link:
                        self.search_twitter(f, post_link)

    def search_twitter(self, f, url):
        text = self.get_twitter_text(url)
        for word in self.keywords:
            if re.search("(?<![\w\d])"+word+"(?![\w\d])", text):
                if (self.url_only):
                    f.write(url + "\n")
                    return
                else:
                    f.write(text + "\n" + "source: " + url + "\n")
                    print("a post containing the key word found")
                    return

    def get_twitter_text(self, url):
        self.driver.get(url)
        time.sleep(self.sleep_for)
        text = ""
        elements = self.driver.find_elements_by_tag_name("span")
        count = 0
        for element in elements:
            text += element.text
        return text

    def crawl(self):

        with open("output.txt", "a") as f:
            f.write("*****INSTAGRAM*****\n\n")

        try:
            print("starting scraping instagram")
            self.instagram()
            print("instagram scraping is complete")
        except:
            print("instagram scraping is incomplete")

        with open("output.txt", "a") as f:
            f.write("*****TWITTER*****\n\n")
        try:
            print("starting scraping twitter")
            self.twitter()
            print("twitter scraping is complete")
        except:
            print("twitter scraping is incomplete")
        self.close()

    def close(self):
        self.driver.close()
        self.driver.quit()
