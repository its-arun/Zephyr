from flask import Flask, render_template
from detector import gogo
import json
from malwareanalysis import malwarescanner

app = Flask(__name__)
app.debug = True
app.secret_key = 'devkey'

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/logscan')
def detector():
    return render_template('logscan.html')

@app.route('/malwarescan')
def malware():
    #data = gogo('access.log')
    return render_template('malwarescan.html', data=data)

@app.route('/loghandler', methods = ['GET', 'POST'])
def loghandler():
   if request.method == 'POST':
      f = request.files['file']
      data = json.loads(gogo(f))
      #f.save(secure_filename(f.filename))
      return render_template('logresult.html', data=data)

@app.route('/malwarehandler', methods = ['GET', 'POST'])
def malwarehandler():
   if request.method == 'POST':
      f = request.files['file']
      data = malwarescanner(f)
      #f.save(secure_filename(f.filename))
      return render_template('malwareresult.html', data=data)

if __name__ == '__main__':
    app.run()