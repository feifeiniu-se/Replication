from random import randint

import numpy
import sklweka.jvm as jvm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.utils import shuffle
from sklweka.dataset import load_arff, to_nominal_labels
from sklweka.classifiers import WekaEstimator
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier

flag = 5

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
    x_train1 = [tmp[2:flag] for tmp in train]
    y_train1 = [tmp[-1] for tmp in train]
    x_test = [tmp[2:flag] for tmp in test]
    y_test = [tmp[-1] for tmp in test]
    # y_train = to_nominal_labels(y_train)
    # y_test = to_nominal_labels(y_test)
    rus = RandomUnderSampler(random_state=1)

    # x_train_ = []
    # y_train_ = []
    # for i in range(len(x_train1)):
    #     if y_train1[i] == 1:
    #         x_train_.append(x_train1[i])
    #         y_train_.append(y_train1[i])
    #     elif y_train1[i] == -1:
    #         if  x_train1[i][2] != 0 and x_train1[i][1] != 0:
    #             x_train_.append(x_train1[i])
    #             y_train_.append(y_train1[i])

    x_train, y_train = rus.fit_resample(x_train1, y_train1)
    # x_train, y_train = rus.fit_resample(x_train_, y_train_)
    x_train, y_train = shuffle(x_train, y_train)


    # clf = DecisionTreeClassifier()
    # clf = DecisionTreeClassifier(criterion="gini", min_samples_split=100, max_depth = 16)
    clf =  MLPClassifier(hidden_layer_sizes=(5,2), max_iter=500, random_state=1, solver="adam", activation='logistic')
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    prob = clf.predict_proba(x_test)
    # feature_imp = clf.tree_.compute_feature_importances(normalize=False)
    # print(feature_imp)
    # prob2 = clf.predict_proba(x_train)
    # print(clf.param)
    if y_pred[0]==-1:
        assert prob[0][0]>=prob[0][1]
    if y_pred[0]==1:
        assert prob[0][0]<=prob[0][1]
    # print("accuracy: ", metrics.accuracy_score(y_test, y_pred))
    # result = [test[i] for i in range(len(test)) if y_pred[i]=="_bug"]
    # prob = [prob[i] for i in range(len(test)) if y_pred[i]=='_bug']
    # # print(len(result))
    # print(confusion_matrix(y_test, y_pred))
    # for i in range(len(y_pred)):
    #     print(str(y_pred[i]) + " " + str(prob[i]))
    # print(prob)
    return [k[1] for k in prob]