BASE_URL = "https://pythonprogramming.net"
import requests
from urllib.parse import urlparse, urlunparse,urljoin
from bs4 import BeautifulSoup

class Crawler():

	def __init__(self, base_url):
		self.base_url = base_url
		self.parsed_base_url = urlparse(base_url)
		self.netloc = self.parsed_base_url.netloc		
		self.links = set()
		self.parsed_links = set()

	def crawl(self):
		soup = self.get_soup(self.base_url)

		for tag in soup.find_all("a"):
			href = tag.get("href")
			href = self.sanitize_href(href, self.base_url).strip().rstrip('/') # Removed trailing /
			parsed_href = urlparse(href)._replace(fragment='')
			if (parsed_href.netloc == self.parsed_base_url.netloc):
				self.links.add(parsed_href.geturl())
	@staticmethod
	def get_soup(website_url):
		html_doc = requests.get(website_url).text.strip()
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
v_bot.crawl()
for link in v_bot.links:
	print(link)