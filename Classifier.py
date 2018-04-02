import scipy.io as sio
from sklearn.model_selection import KFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn import tree
from sklearn import neighbors
from sklearn import preprocessing
import numpy as np
import random
from sklearn.metrics import confusion_matrix



def LDA(filePath,iterNum,nfold):

    variableName = "afterSGSmooth"
    mat = sio.loadmat(filePath)
    data = mat[variableName]
    newData = data[:256,:].T
    label = data[256,:].T
    matrix = []
    acc=0
    for i in np.arange(0,iterNum,1):
        kf = KFold(n_splits=nfold, shuffle=True)
        for trainIdx,testIdx in kf.split(label):
            X_train, X_test, y_train, y_test = \
                newData[trainIdx,:],newData[testIdx,:],label[trainIdx],label[testIdx]
            clf = LinearDiscriminantAnalysis()
            clf.fit(X_train, y_train)
            matrix.append(confusion_matrix(y_test, clf.predict(X_test)))
            acc += clf.score(X_test,y_test)
    return acc/(nfold*iterNum),matrix

def SVM(filePath,iterNum,nfold):

    variableName = "afterSGSmooth"
    mat = sio.loadmat(filePath)
    data = mat[variableName]
    newData = data[:256, :].T
    newData = preprocessing.scale(newData)
    label = data[256, :].T
    matrix = []
    acc = 0
    for i in np.arange(0,iterNum,1):
        kf = KFold(n_splits=nfold, shuffle=True)
        for trainIdx,testIdx in kf.split(label):
            X_train, X_test, y_train, y_test = \
                newData[trainIdx,:],newData[testIdx,:],label[trainIdx],label[testIdx]
            clf = SVC(kernel="linear")
            clf.fit(X_train, y_train)
            matrix.append(confusion_matrix(y_test, clf.predict(X_test)))
            acc += clf.score(X_test,y_test)
    return acc / (nfold * iterNum),matrix

def KNN(filePath,iterNum,nfold):

    variableName = "afterSGSmooth"
    mat = sio.loadmat(filePath)
    data = mat[variableName]
    newData = data[:256, :].T
    newData = preprocessing.scale(newData)
    label = data[256, :].T
    matrix = []
    acc = 0
    for i in np.arange(0,iterNum,1):
        kf = KFold(n_splits=nfold, shuffle=True)
        for trainIdx,testIdx in kf.split(label):
            X_train, X_test, y_train, y_test = \
                newData[trainIdx,:],newData[testIdx,:],label[trainIdx],label[testIdx]
            clf = neighbors.KNeighborsClassifier(1)
            clf.fit(X_train, y_train)
            matrix.append(confusion_matrix(y_test, clf.predict(X_test)))
            acc += clf.score(X_test,y_test)
    return acc / (nfold * iterNum),matrix

def DT(filePath,iterNum,nfold):

    variableName = "afterSGSmooth"
    mat = sio.loadmat(filePath)
    data = mat[variableName]
    newData = data[:256, :].T
    newData = preprocessing.scale(newData)
    label = data[256, :].T
    matrix = []
    acc = 0
    for i in np.arange(0, iterNum, 1):
        kf = KFold(n_splits=nfold, shuffle=True)
        for trainIdx, testIdx in kf.split(label):
            X_train, X_test, y_train, y_test = \
                newData[trainIdx, :], newData[testIdx, :], label[trainIdx], label[testIdx]
            clf = tree.DecisionTreeClassifier()
            clf.fit(X_train, y_train)
            matrix.append(confusion_matrix(y_test, clf.predict(X_test)))
            acc += clf.score(X_test, y_test)
    return acc / (nfold * iterNum),matrix

def SDE(filePath,nfold,numLearn,numWave):

    variableName = "afterSGSmooth"
    mat = sio.loadmat(filePath)
    data = mat[variableName]
    newData = data[:256, :].T
    label = data[256, :].T
    matrix = []
    acc = 0

    kf = KFold(n_splits=nfold, shuffle=True)
    for trainIdx, testIdx in kf.split(label):
        for i in np.arange(0, numLearn, 1):  #多少个弱分类器
            list = np.arange(0, 256, 1).tolist()
            ramList = random.sample(list,numWave)  #选多少个波段
            newData = newData[:,ramList]
            newLabel = label
            X_train, X_test, y_train, y_test = \
                newData[trainIdx, :], newData[testIdx, :], newLabel[trainIdx], newLabel[testIdx]
            lda = LinearDiscriminantAnalysis()
            lda.fit(X_train, y_train)
            matrix.append(confusion_matrix(y_test, lda.predict(X_test)))
            acc += lda.score(X_test, y_test, sample_weight=None)

    return acc / (nfold * numLearn),matrix
