from flask import Flask, render_template, redirect, request
from storage import get_entries, add_entry, get_answer

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
    return render_template('home.html', input_field_state='neutral', entries=get_entries())


# request some path probably stored before
@app.route('/<path>')
def go_to_path(path):
    if get_answer(path):
        return redirect(get_answer(path)), 302
    return render_template('404.html')


# try to create new
@app.route("/create_short_url", methods=["POST"])
def new_short_url():
    longurl = request.form['input']
    print(longurl)
    return redirect('/')


if __name__ == '__main__':
    app.run()