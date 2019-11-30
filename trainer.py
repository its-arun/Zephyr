from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn import metrics
import urllib.parse
import json

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
def starttraining():
    def loadFile(name):
        directory = str(os.getcwd())
        filepath = os.path.join(directory, name)
        with open(filepath,'r', errors='ignore') as f:
            data = f.readlines()
        data = list(set(data))
        result = []
        for d in data:
            d = str(urllib.parse.unquote(d))   #converting url encoded data to simple string
            result.append(d)
        return result

    badQueries = loadFile('badqueries.txt')
    validQueries = loadFile('goodqueries.txt')

    badQueries = list(set(badQueries))
    validQueries = list(set(validQueries))
    allQueries = badQueries + validQueries
    yBad = [1 for i in range(0, len(badQueries))]  #labels, 1 for malicious and 0 for clean
    yGood = [0 for i in range(0, len(validQueries))]
    y = yBad + yGood

    queries = allQueries

    vectorizer = TfidfVectorizer(min_df = 0.0, analyzer="char", sublinear_tf=True, ngram_range=(1,3)) #converting data to vectors
    X = vectorizer.fit_transform(queries)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #splitting data

    badCount = len(badQueries)
    validCount = len(validQueries)

    lgs = LogisticRegression(class_weight={1: 2 * validCount / badCount, 0: 1.0}) # class_weight='balanced')

    lgs.fit(X_train, y_train) #training our model
    joblib.dump(lgs, 'trainedmodel.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    ##############
    # Evaluation #
    ##############=
    predicted = lgs.predict(X_test)

    fpr, tpr, _ = metrics.roc_curve(y_test, (lgs.predict_proba(X_test)[:, 1]))
    auc = metrics.auc(fpr, tpr)

    outtoret = {}

    outtoret.update({"Bad-samples": badCount})
    outtoret.update({"Good-samples": validCount})
    outtoret.update({"Baseline-Constant-negative":(validCount / (validCount + badCount))})
    outtoret.update({"Accuracy":lgs.score(X_test, y_test)})  #checking the accuracy
    outtoret.update({"Precision": metrics.precision_score(y_test, predicted)})
    outtoret.update({"Recall": metrics.recall_score(y_test, predicted)})
    outtoret.update({"F1-Score": metrics.f1_score(y_test, predicted)})
    outtoret.update({"AUC":auc})

    return json.dumps(outtoret)