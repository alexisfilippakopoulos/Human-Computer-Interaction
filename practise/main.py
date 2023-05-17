from random import random
from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
from RandomForest import RandomForest
from DecisionTree import DecisionTree
import pandas as pd

"""
data = datasets.load_breast_cancer()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1234
)
print(X_train, y_train)
"""
l1 = [0, 1, 1, 1]
l2 = [0, 1, 1, 0]
l3 = [0, 1, 0, 1]
l4 = [0, 0, 1, 0]


X_train = np.array([l1, l2, l3, l4])
y_train = np.array([0, 1, 0, 1])

l1 = [0, 0, 0, 0]
l2 = [1, 1, 1, 1]

X_test = np.array([l1, l2])
y_test = np.array([0, 1])

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    #print(y_true == y_pred)
    print(y_pred)
    return accuracy

clf = RandomForest()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
#print(X_train[0])
#print (y_train)
"""
clf = DecisionTree()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
"""
acc =  accuracy(y_test, predictions)
print(acc)