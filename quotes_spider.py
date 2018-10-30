import requests
from bs4 import BeautifulSoup
import csv
import re

class QuotesSpider(object):

    def __init__(self, url='http://quotes.toscrape.com', crawl=None, depth=None, file_path='quotes.csv'):
        self.response = requests.get(url)
        self.crawl = crawl
        self.depth = depth
        self.csv_file = open(file_path, "w")
        self.writer = csv.writer(self.csv_file)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        authors = [a.get_text() for a in soup.find_all(class_="author")]
        quotes = [q.get_text() for q in soup.find_all(class_='text')]
        data = zip(authors, quotes)
        for row in data:
            self.writer.writerow(row)
        if self.crawl or self.depth:
            if self.depth:
                if self.depth == 0:
                    return
                self.depth -= 1
            base_url = re.compile(r"(http://[a-zA-Z.]+)").findall(response.url)[0]
            nxt_link = soup.find(class_='next')
            if nxt_link is not None:
                nxt_url = base_url + nxt_link.find(name='a', href=re.compile(r"^/page/[0-9]+/")).attrs['href']
                print(nxt_url)
                response = requests.get(nxt_url)
                self.parse(response)

    def run(self):
        print("scraper started...")
        self.parse(self.response)
        self.csv_file.close()
        print("Done...")


if __name__ == '__main__':
    spider = QuotesSpider(crawl=True)
    spider.run()
