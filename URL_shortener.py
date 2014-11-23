from flask import Flask, render_template, redirect, request
from storage import get_entries, add_entry

app = Flask(__name__)

'''
<-- TEST -->
print(get_entries())
add_entry({
        'short_url': '<domain>.com/google',
        'long_url': 'http://google.com',
        'ip' : '0.0.0.0'
})
print(get_entries())
'''

@app.route('/')
def get_home():
    return render_template('home.html', input_field_state = 'neutral', entries = [])

@app.route('/<path>')
def go_to_path(path):
    #TODO: check if path is valid or not and then handle it
    return render_template('404.html')

@app.route("/create_long_url", methods=["POST"])
def new_long_url():
    longURL = request.form['input']
    print(longURL)
    return redirect('/')

if __name__ == '__main__':
    app.run()