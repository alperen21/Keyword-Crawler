# Keyword Crawler

## Motivation behind this project

The main motivation behind this project was a desire for automation.
I volunteer at the Sponsorships department of a students' club and whenever we have a meeting with a company, we first need to browse through social media accounts of companies to see what kind of sponsor-relations they have established with other student clubs. Doing that is a very labor-intensive and mechanical task so I wrote this simple script to do that for me. This is also why the original name of the class was "Sponsorship Crawler" but then I renamed it to have a more general name.

## Tools used for this project

What this script does is to browse through multiple social media accounts (Instagram and Twitter because they seem to be most relevant choices for this) of multiple students' clubs and write urls / texts of the posts if they contain predetermined keywords.

The library I used is Selenium because of Javascript implementation on both Twitter and Instagram. Twitter and Instagram pages are dynamically created with Javascript so using requests library is pretty much out of the question. But using a vanilla version of Selenium is also a bit troublesome since I did not want to deal with an additional window opening on my computer everytime I run this script. So, I used Selenium with headless Firefox (you also need to install Geckodriver to make this script work). I originally also thought of using BeautifulSoup to parse data but as it turns out, it's not particularly necessary for this project.

## Flow of the script

### Setup

#### search.json and login.json

Search.json and login.json files are prerequisites of this script. It is best to use environment variables to store password / username information. login.json file needs to include names of the username/password environment variables of respective social media websites. An example login.json file is included in this repository.

Search.json file contains which urls are to be visited for each social media account (the list can be left empty if you do not want the script to visit that website) and a list of keywords. Keywords are case insensitive but there must be an exact match for the script to consider the page to be relevant (for example if you type "App" as a keyword, a page that contains "You can find this app on Google Playstore" will be included in the output but "New Apple Store in Istanbul" will not be included)

#### instantiation

The class requires couple arguments to be instantiated even though most of them have a default value. Here are the arguments:

- gecko_directory: Does not have a default value. You need to pass directory of the geckodriver. A raw string is preffered.

- login_directory: Directory of login.json file. If no argument is given the class will assume that there is a login.json file in the working directory.

- search_directory: Directory of search.json file. If no argument is given the class will assume that there is a search.json file in the working directory.

- sleep_for: Selenium needs to sleep for couple seconds before it starts grabbing elements because the page needs to load first. A big value for sleep_for parameter (in seconds) will ensure Selenium does not try to grab elements too early (which will result in a crash) but it will also make the whole execution a lot more sluggish. A small value for sleep_for will make the whole process faster but it is also riskier especially if you have a bad internet connection.

* depth: How deep down the posts you want the script to go? My recommendation for this is a value between 1 to 3 since a huge number for this may cause an infinite loop.

* url_only: If set to True (default value) the scrip will output only the urls of the relevant pages it found. If set to False, it will include relevant texts of the pages too (not recommended).

#### output.txt

After the execution, the script will write the information it found on output.txt file. You do not need to have one in your directory; if absent, the script will create one.

### Execution

After the instantiation of the class, you only need to call crawl() method on the instance of this class and nothing else.

Crawl method will invoke instagram() and twitter() methods sequentially inside try blocks so that if the search.json does not contain anything in terms of twitter / instagram etc. it will get a key error and instead of stopping the execution, the code will just switch to the next function.

Inside the twitter and instagram functions, the code will first login using Environment variables. KeywordCrawler class is inherited from EnvLoginGatherer so for more information for login process feel free to inspect EnvLoginGatherer.py file.

Then the file will go to the homepage of respective social media accounts and will extract links for posts / tweets. Then, it will sequentially visit those sites and will utilize Regular Expressions to test if they contain any of the keywords and if they do, their urls (and texts if url_only is initialized to false) will be written in output.txt file.

The code will notify the user throught this process using the console.

An example source file and an example output.txt are also included in this repository.

### References

- Instagram webscraping: https://medium.com/swlh/tutorial-web-scraping-instagrams-most-precious-resource-corgis-235bf0389b0c

- Regex: https://stackoverflow.com/questions/5752829/regular-expression-for-exact-match-of-a-string

### Disclaimer

This script was created for something legal and innocent (automating a research task). I bear no responsibility for the misuse of this code. Also you should know that extracting a massive amount of data using this or any other webscraping tool might be considered illegal in some websites / countries.
