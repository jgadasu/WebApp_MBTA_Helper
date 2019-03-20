from flask import Flask, render_template, request

from mbta import find_stop_nears

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    if name:
        name = name.upper()
    return render_template('hello.html', name=name)


@app.route('/calc/', methods=['GET', 'POST'])


def find_stop_near():
    if request.method == 'POST':

        place_name = (request.form['place_name'])

        answer = find_stop_nears(place_name)

        if answer:
            return render_template('calculator_result.html', answer=answer)
        else:
            return render_template('calculator_form.html', error=True)
    return render_template('mbta.html', error=None)
