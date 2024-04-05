#!/usr/bin/python3
import sys
import bs4 as bs
import urllib.request
import validators
from urllib.parse import urlparse


def is_valid_url(url):
    return validators.url(url)


def get_soup(base_url):
    source = urllib.request.urlopen(base_url).read()
    soup = bs.BeautifulSoup(source, 'html.parser')
    return soup


def get_urls(soup):
    return soup.find_all(href=True)


def parse_url(url, base_url, same_base_url=True):
    parsed_base_url = urlparse(base_url)
    base_url = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}".rstrip('/')

    if url.startswith("/"):
        return base_url + url
    elif not url.startswith("http"):
        return f"{base_url}/{url}"
    else:
        return url


def parse_urls(urls, base_url, same_hostname=True):
    urls = [parse_url(url["href"], base_url) for url in urls]
    if (same_hostname):
        return [url for url in urls if urlparse(url).hostname == urlparse(base_url).hostname]
    else:
        return urls


if __name__ == "__main__":
    if len(sys.argv) == 2:
        base_url = sys.argv[1]
    else:
        base_url = 'https://vrindavansanap.github.io/index.html'

    if not validators.url(base_url):
        print("Invalid URL. Please provide a valid URL.")
        sys.exit(1)

    program_name = "URLs Finder"
    welcome_message = "🚀 Welcome! This program is designed to discover and list all URLs present on the webpage you specify. Let's dive in!"

    print(program_name)
    print(welcome_message)
    print(f"Scraping: {base_url} \n")
    soup = get_soup(base_url)
    title = soup.title.text
    print(f"Title: {title}")
    urls = get_urls(soup)
    parsed_urls = parse_urls(urls, base_url)
    for url in parsed_urls:
        print(f"{url}")

    print(f"{len(parsed_urls)} urls found!!")
