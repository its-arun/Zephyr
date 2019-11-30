import joblib
import urllib.parse
import re
import json

def gogo(infile_name):
    parsed_uri = []
    all_logs = []
    pretty_logs = []

    def log_parser(logfile):
        ip_regex = r"^\d{1,3}\W\d{1,3}\W\d{1,3}\W\d{1,3}"
        date_regex = r"\[(.*?)\]"
        uri_regex = r'"(.*?)"'
        response_regex = r"\"\s\d{3}"
        bytes_regex = r"\"\s\d{3}\s\d{0,6}"
        temp = {}
        for logs in logfile:
            ip = re.findall(ip_regex, logs)[0]
            date = re.findall(date_regex, logs)[0]
            uri = re.findall(uri_regex, logs)[0]
            useragent = re.findall(uri_regex, logs)[2]
            response_code = re.findall(response_regex, logs)[0].split()[1]
            resbytes = re.findall(bytes_regex, logs)[0].split()[2]
            temp = {'IP': ip, 'Date': date, 'Request': uri, 'User-Agent': useragent, 'Response': response_code, 'Transferred': resbytes}
            pretty_logs.append(temp)
        #print(pretty_logs)

    #log cleaning with regex
    def uri_parser(logfile):
        regex = r'"(.*?)"'
        for line in logfile:
            all_logs.append(line.rstrip())
            if 'GET' in line:
                parsed_uri.append(re.findall(regex, line)[0][4:-9])
            elif 'POST' in line:
                parsed_uri.append(re.findall(regex, line)[0][5:-9])

    #load models
    lgs = joblib.load('trainedmodel.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    #do the magic
    infile = open(infile_name, 'r')
    uri_parser(infile)
    log_parser(open(infile_name, 'r'))

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
            pretty_logs[i].update({'Verdict': 'Clean'})
        elif _ == 1:
            pretty_logs[i].update({'Verdict': 'Malicious'})
        i += 1

    return json.dumps(pretty_logs)
