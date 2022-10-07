from random import randint

import numpy
import sklweka.jvm as jvm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.utils import shuffle
from sklweka.dataset import load_arff, to_nominal_labels
from sklweka.classifiers import WekaEstimator
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier

flag_refactor = False
if flag_refactor==True:
    flag = -1
else:
    flag = 5
    # flag = 49

def J48(train, test):
    jvm.start(packages=True)
    x_train = [tmp[2:flag] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:flag] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    y_train = to_nominal_labels(y_train)
    y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)
    x_train, y_train = rus.fit_resample(x_train, y_train)

    j48 = WekaEstimator(classname="weka.classifiers.trees.J48", options=["-C", "0.5"])
    j48.fit(x_train, y_train)
    y_pred = j48.predict(x_test)
    prob = j48.predict_proba(x_test)
    # result = [test[i] for i in range(len(test)) if scores[i]=="_bug"]
    if y_pred[0] == '_bug':
        assert prob[0][0] > prob[0][1]
    if y_pred[0] == '_no_bug':
        assert prob[0][0] < prob[0][1]

    jvm.stop()
    return prob

def DT(train, test):
    x_train = [tmp[2:flag] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:flag] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    y_train = to_nominal_labels(y_train)
    y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)
    x_train, y_train = rus.fit_resample(x_train, y_train)

    clf = DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    prob = clf.predict_proba(x_test)
    if y_pred[0]=='_bug':
        assert prob[0][0]>prob[0][1]
    if y_pred[0]=='_no_bug':
        assert prob[0][0]<prob[0][1]
    # print("accuracy: ", metrics.accuracy_score(y_test, y_pred))
    # result = [test[i] for i in range(len(test)) if y_pred[i]=="_bug"]
    # prob = [prob[i] for i in range(len(test)) if y_pred[i]=='_bug']
    # # print(len(result))
    # print(confusion_matrix(y_test, y_pred))
    # for i in range(len(y_pred)):
    #     print(str(y_pred[i]) + " " + str(prob[i]))
    # print(prob)
    return [k[1] for k in prob]

def MLP(train, test):
    x_train = [tmp[2:-1] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:-1] for tmp in test]
    y_test = [tmp[-1] for tmp in test]

    y_train = to_nominal_labels(y_train)
    y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)
    # print(x_train[0])
    x_train, y_train = rus.fit_resample(x_train, y_train)
    x_train, y_train = shuffle(x_train, y_train)

    mlp = MLPClassifier(hidden_layer_sizes=(3,2), max_iter=500, random_state=1, solver="adam", activation='logistic') # some projects have the best result tanh(hornetq) logistic(izpack)
    # mlp = MLPClassifier(hidden_layer_sizes=(5,2), max_iter=500, random_state=1, solver="adam", activation='logistic') # some projects have the best result tanh(hornetq) logistic(izpack)
    # mlp = MLPClassifier(hidden_layer_sizes=(32,2), random_state=1, max_iter=500, solver="adam", activation='logistic')
    mlp.fit(x_train, y_train)
    # print(mlp.best_params_)
    y_pred = mlp.predict(x_test)
    prob = mlp.predict_proba(x_test)
    # print(y_pred)
    if y_pred[0] == '_bug':
        assert prob[0][0] > prob[0][1]
    if y_pred[0] == '_no_bug':
        assert prob[0][0] < prob[0][1]
    return [k[0] for k in prob]
    # return result

def RF(train, test):
    x_train = [tmp[2:flag] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:flag] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    y_train = to_nominal_labels(y_train)
    y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)
    x_train, y_train = rus.fit_resample(x_train, y_train)

    rf = RandomForestClassifier(random_state=1)
    rf.fit(x_train, y_train)
    y_pred = rf.predict(x_test)
    prob = rf.predict_proba(x_test)
    # print(y_pred)
    if y_pred[0] == '_bug':
        assert prob[0][0] > prob[0][1]
    if y_pred[0] == '_no_bug':
        assert prob[0][0] < prob[0][1]
    return prob

def MLPLogistic(train, test):
    x_train = [tmp[2:5] for tmp in train]
    y_train = [tmp[-1] for tmp in train]
    x_test = [tmp[2:5] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    y_train = [1 if k == 'bug' else 0 for k in y_train]
    y_test = [1 if k == 'bug' else 0 for k in y_test]
    rus = RandomUnderSampler(random_state=1)
    x_train, y_train = rus.fit_resample(x_train, y_train)
    x_train, y_train = shuffle(x_train, y_train)


    mlp = MLPRegressor(hidden_layer_sizes=(3), activation='logistic', solver='adam')
    mlp.fit(x_train, y_train)
    y_pred = mlp.predict(x_test)
    return y_pred