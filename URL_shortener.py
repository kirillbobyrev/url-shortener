from flask import Flask, render_template, redirect, request, json, current_app, url_for
from storage import get_entries, add_entry, get_answer
import re
import random

app = Flask(__name__)

CHARSET = 'qwertyuiopasdfghjklzxcvbnmm1234567890'

@app.route('/')
def get_home():
    cookies = request.cookies.get('cookies')
    print(cookies)
    if cookies != None:
        cookies = json.loads(cookies)
    return render_template('home.html', cookies=cookies)


@app.route('/<path>')
def go_to_path(path):
    if get_answer(path):
        return redirect(get_answer(path)), 302
    return render_template('404.html')


@app.route("/create_short_url", methods=["POST"])
def create_short_url():
    long_url = request.form.getlist('long_url')
    if len(long_url) != 0:
        long_url = long_url[0]
    else: long_url = ''
    short_specify = request.form.getlist('short_url_specified')
    short_url = ''
    if 'on' in short_specify:
        short_url = request.form.getlist('short_url')
        if len(short_url) != 0:
            short_url = short_url[0]
        else: short_url = ''
    elif valid_url(long_url):
        short_url = ''.join(random.choice(CHARSET) for _ in range(5))
        # returns false only if no such short_url exists in storage
        while get_answer(short_url):
            short_url = ''.join(random.choice(CHARSET) for _ in range(5))

    redirect_to_index = redirect('/')
    response = current_app.make_response(redirect_to_index)
    cookie = {'short_url': short_url, 'long_url': long_url,
                                        'short_specify': 'on' in short_specify, 'HOST_URL': request.url_root}

    if valid_url(long_url) and not get_answer(short_url):
        cookie['status'] = 'success'
        add_entry({
            'short_url': short_url,
            'long_url': long_url
        })
    elif get_answer(short_url):
        cookie['status'] = 'already-exists'
    else:
        cookie['status'] = 'invalid-url'
    response.set_cookie('cookies', json.dumps(cookie))
    print(cookie)
    return response

def valid_url(url):
    if url == '' or url == []:
        return False
    if 'http:/' not in url and 'https:/' not in url:
        url = 'http:/' + url
    return re.match(r'^[a-zA-Z]+://', url)

if __name__ == '__main__':
    app.debug = True
    app.run()