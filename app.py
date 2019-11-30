from flask import Flask, render_template, request
from detector import gogo
import json
from malwareanalysis import malwarescanner
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = './uploads'
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
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      data = json.loads(gogo(os.path.join(app.config['UPLOAD_FOLDER'],filename)))
      os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
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