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
    #infile_name = 'access.log'
    infile = open(infile_name, 'r')
    uri_parser(infile)
    #list of dictionaries
    output = []
    X_predict = parsed_uri
    X_predict = vectorizer.transform(X_predict)
    y_Predict = lgs.predict(X_predict)
    prediction = y_Predict.tolist()
    print(prediction)

    for _ in prediction:
        temp = {}
        if prediction[_] == 0:
            temp = { all_logs[_] : 'Clean' }
        elif prediction[_] == 1:
            temp = { all_logs[_] : ' Malicious' }
        output.append(temp)

    return json.dumps(output)
    #return all_logs

#debugging

#print(gogo('access.log'))
