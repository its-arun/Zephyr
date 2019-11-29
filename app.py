from flask import Flask, render_template
from detector import gogo
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'devkey'

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/detector')
def detector():
    data = json.loads(gogo('access.log'))
    #data = gogo('access.log')
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()