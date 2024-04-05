import time
from list_all_urls import *


from flask import Flask, render_template, request
import validators
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        st = time.time()
        # Process form data
        print(request.form)
        base_url = request.form["url_input"]
        if not is_valid_url(base_url):
            if not is_valid_url("https://www."+base_url):
                if not is_valid_url("https://"+base_url):
                    error = "Invalid url"
                    time_taken = time.time() - st
                    return render_template('form.html', url=base_url, time_taken=time_taken, error=error)
                else:
                    base_url = "https://"+base_url
            else:
                base_url = "https://www."+base_url
        print(base_url)
        error = ""
        soup = get_soup(base_url)
        urls = get_urls(soup)
        urls = parse_urls(urls, base_url)
        time_taken = time.time() - st
        return render_template('form.html', url=base_url, time_taken=time_taken, error=error, urls=urls)

    else:
        # Display the empty form
        error = ""
        url = "hello"
        return render_template('form.html', url=url, error=error)
