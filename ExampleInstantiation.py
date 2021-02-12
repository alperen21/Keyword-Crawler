from crawler import KeywordCrawler

try:
    crawler = KeywordCrawler(
        r'/Users/alperen/Desktop/geckodriver', depth=1, url_only=False)
    crawler.crawl()
except KeyboardInterrupt:  # except blocks will ensure that Selenium will be closed properly even if you or an error stops the code-run mid-execution
    crawler.close()
    print("crawler closed due to keyboard intteruption")
except:
    crawler.close()
    print("Something went wrong")
