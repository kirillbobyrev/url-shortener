from flask import Flask, render_template, redirect, request
from storage import get_entries, add_entry, get_answer
import random
from urllib.parse import urlparse
import re

app = Flask(__name__)


# TODO: add IP to entry info and print out 10 last links made by user with current IP
'''
# <!-- TEST -->
print(get_entries())
add_entry({
        'short_url': '<domain>.com/google',
        'long_url': 'http://google.com',
})
print(get_entries())
'''

# GLOBALS
long_url = ''
specify_url=False
short_url = ''
successful_request=True
returned_message = ''
#

@app.route('/')
def get_home():
    print('Entries:\n', get_entries())
    # add some params that page appearance will depend on
    return render_template('home.html', long_url=long_url, specify_url=specify_url, short_url=short_url,
                           successful_request=successful_request, returned_message=returned_message)


# request some path probably stored before
@app.route('/<path>')
def go_to_path(path):
    if get_answer(path):
        return redirect(get_answer(path)), 302
    return render_template('404.html')


# try to create new
@app.route("/create_short_url", methods=["POST"])
def create_short_url():
    # TODO:ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    global long_url, specify_url, short_url, successful_request, returned_message
    returned_short_specify = ''
    returned_long_url = ''
    returned_short_url = ''
    try:
        returned_long_url = request.form['long_url']
        returned_short_specify = request.form['short_url_specified']
        returned_short_url = request.form['custom_short_tb']
    except:
        pass

    print('long_url:', returned_long_url)
    print('short_specified:', returned_short_specify)
    print('short_url:', returned_short_url)

    if returned_short_specify == 'on' and returned_short_url != '' and valid_url(returned_long_url):
        add_entry({
            'short_url': returned_short_url,
            'long_url': returned_long_url,
        })
        returned_message = urlparse(request.url_root).hostname

        successful_request = True
    elif returned_short_specify != 'on' and valid_url(returned_long_url):
        add_entry({
            'short_url': returned_short_url,
            'long_url': returned_long_url,
        })
        returned_message = urlparse(request.url_root).hostname

    long_url = returned_long_url
    short_url = returned_short_url
    specify_url = returned_short_specify == 'on'

    return redirect('/')


def valid_url(url):
    if 'http:/' not in url:
        url += 'http:/'
    return re.match(r'^[a-zA-Z]+://', url)

if __name__ == '__main__':
    app.run()