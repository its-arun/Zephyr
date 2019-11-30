import joblib
import urllib.parse
import re
import json

def gogo(infile_name):
    parsed_uri = []
    all_logs = []

    #log cleaning with regex
    def uri_parser(logfile):
        regex = r'"(.*?)"'
        for line in logfile:
            all_logs.append(line.rstrip())
            if 'GET' in line:
                parsed_uri.append(re.findall(regex, line)[0][4:-9])
            elif 'POST' in line:
                parsed_uri.append(re.findall(regex, line)[0][5:-9])
        #print(parsed_uri)

    #load models
    lgs = joblib.load('trainedmodel.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    #do the magic
    infile = open(infile_name, 'r')
    uri_parser(infile)
    
    #list of dictionaries
    output = []
    X_predict = parsed_uri
    X_predict = vectorizer.transform(X_predict)
    y_Predict = lgs.predict(X_predict)
    prediction = y_Predict.tolist()
    
    i = 0
    for _ in prediction:
        temp = {}
        if _ == 0:
            temp = { all_logs[i] : 'Clean' }
        elif _ == 1:
            temp = { all_logs[i] : ' Malicious' }
        output.append(temp)
        i += 1

    return json.dumps(output)
