import sqlite3
con = sqlite3.connect("crawled.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS websites(
        netloc TEXT,
        endpoint TEXT,
        size INTEGER,
        webpage_content TEXT
    )
""")

BASE_URL = "https://pythonprogramming.net"
import requests
from urllib.parse import urlparse, urlunparse,urljoin
from bs4 import BeautifulSoup

class Crawler():

	def __init__(self, base_url):
		self.base_url = base_url
		self.parsed_base_url = urlparse(base_url)
		self.netloc = self.parsed_base_url.netloc		
		self.parsed_links = set()
		self.parsed_links.add(self.parsed_base_url)
		self.crawled_links = set()

	def crawl(self):
		while (len(self.parsed_links) != 0):
			if len(self.parsed_links) == 0:
				return 
			link = self.parsed_links.pop()
			print(f"Crawling {link.geturl()} -{len(self.crawled_links)}/{len(self.parsed_links)}")
			html_doc = self.get_html_doc(link.geturl())
			cur.execute("""INSERT INTO websites (netloc, endpoint, size, webpage_content) VALUES (?, ?, ?, ?)
			""", (link.netloc, link.path, len(html_doc), html_doc))
			con.commit()


			soup = self.get_soup(html_doc)
			for tag in soup.find_all("a"):
				href = tag.get("href")
				href = self.sanitize_href(href, self.base_url).strip().rstrip('/') 
				parsed_link = urlparse(href)._replace(fragment='')
				if self.same_base_url(parsed_link):
					if not parsed_link in self.crawled_links:
						self.parsed_links.add(parsed_link)
			self.crawled_links.add(link)

	def same_base_url(self, link):
		if (link.netloc == self.parsed_base_url.netloc):
			return True

	@staticmethod
	def get_html_doc(link):
		html_doc = requests.get(link).text.strip()
		return html_doc 


	@staticmethod
	def get_soup(html_doc):
		soup = BeautifulSoup(html_doc, "html.parser")
		return soup

	@staticmethod
	def has_base_url(url):
		parsed_url = urlparse(url)
		if parsed_url.scheme and parsed_url.netloc:
			return True
		else:
			return False

	@staticmethod
	def sanitize_href(href, base_url):
		if Crawler.has_base_url(href):
			return href
		else:
			return urljoin(base_url, href)


v_bot = Crawler(BASE_URL)
print(v_bot.parsed_links)
v_bot.crawl() 
print(v_bot.parsed_links)