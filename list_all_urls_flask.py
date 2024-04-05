import time
from list_all_urls import *
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect
import validators
app = Flask(__name__)


def parse_base_url(base_url):
    if not is_valid_url(base_url):
        if not is_valid_url("https://www."+base_url):
            if not is_valid_url("https://"+base_url):
                return False
            else:
                base_url = "https://"+base_url
        else:
            base_url = "https://www."+base_url
    return base_url


same_hostname = "checked"


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        st = time.time()
        # Process form data
        base_url = request.form["url_input"]
        global same_hostname
        same_hostname = request.form.get("same_hostname_checkbox")
        base_url = parse_base_url(base_url)
        error = "Invalid url"
        if (not base_url):
            time_taken = time.time() - st
            return render_template('form.html', url=base_url, time_taken=time_taken, error=error, same_hostname=same_hostname)

        error = ""
        soup = get_soup(base_url)
        urls = get_urls(soup)
        urls = parse_urls(urls, base_url, same_hostname)
        urls = list(set(urls))
        n_same_hostname = 0

        for url in urls:
            base_url_hostname = urlparse(base_url).hostname
            if urlparse(url).hostname == base_url_hostname:
                n_same_hostname += 1

        time_taken = time.time() - st
        return render_template('form.html', url=base_url, time_taken=time_taken, n_same_hostname=n_same_hostname, error=error, urls=urls, same_hostname=same_hostname)

    else:
        # Display the empty form
        error = ""
        url = "google.com"
        return render_template('form.html', url=url, error=error, time_taken=0, n_same_hostname=0)
