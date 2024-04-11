#!/usr/bin/python3
import time
from list_all_urls import *
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect
import validators
app = Flask(__name__)


def parse_base_url(base_url):
    if is_valid_url(base_url):
        return base_url

    if not base_url.startswith("https://www."):
        if is_valid_url("https://www." + base_url):
            return "https://www." + base_url

    if not base_url.startswith("https://"):
        if is_valid_url("https://" + base_url):
            return "https://" + base_url

    return False


same_hostname = "checked"


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        start_time = time.time()
        base_url = request.form.get("url_input")
        same_hostname = request.form.get("same_hostname_checkbox")
        base_url = parse_base_url(base_url)

        error = "Invalid URL"
        if not base_url:
            time_taken = time.time() - start_time
            return render_template('form.html', url=base_url, time_taken=time_taken, error=error, same_hostname=same_hostname)

        error = ""
        soup = get_soup(base_url)
        urls = parse_urls(get_urls(soup), base_url, same_hostname)
        urls = list(set(urls))

        n_same_hostname = sum(1 for url in urls if urlparse(
            url).hostname == urlparse(base_url).hostname)

        time_taken = time.time() - start_time
        return render_template('form.html', url=base_url, time_taken=time_taken, n_same_hostname=n_same_hostname, error=error, urls=urls, same_hostname=same_hostname)

    else:
        # Display the empty form
        error = ""
        url = "google.com"
        return render_template('form.html', url=url, error=error, time_taken=0, n_same_hostname=0)
