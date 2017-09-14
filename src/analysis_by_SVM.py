# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:46:19 2017

@author: Jungwon Lee
"""

import os
import pandas as pd
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from scipy import sparse, io
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Twitter

# import pyspark 
import findspark
findspark.init()
import pyspark
sc = pyspark.SparkContext(appName="Pi") 


# RDD 생성
train = sc.textFile("/user/data/Test_Train_set/train.csv")
test = sc.textFile("/user/data/Test_Train_set/test.csv")


# .csv에서 리뷰,라벨만 가져온 RDD 생성(필요x)
x_train = list([x for x in train.map(lambda x:x[:-3]).toLocalIterator()])
y_train = list([x for x in train.map(lambda x:x[-1:]).toLocalIterator()])
#x_test =
#y_test =


# 형태소분석 함수
twit = Twitter()
def tokenizer(text):
    return twit.morphs(text)


# train.csv에서 리뷰만 가져와서 벡터화
vect_1_3 = TfidfVectorizer(ngram_range=(1,5), min_df = 3, tokenizer=tokenizer).fit(x_train)

nx_train_1_3 = vect_1_3.transform(x_train)


# SVM 최적옵션 찾기
def svc_param_selection(X, y, nfolds):
    Cs = [0.01, 0.1, 1, 10]
    gammas = [0.01, 0.1, 1]
    param_grid = {'C': Cs, 'gamma' : gammas}
    grid_search = GridSearchCV(svm.SVC(kernel='rbf'), param_grid, cv=nfolds)
    grid_search.fit(X, y)
    grid_search.best_params_
    return grid_search.best_params_

print(svc_param_selection(nx_train_1_3, y_train, 5))


# 최적옵션으로 SVM 정의
clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(nx_train_1_3, y_train)

print(clf.best_score_) #0.8835733333
print(clf.best_params_) # C : 10 , penalty = 'l2'



#머신러닝 결과 저장
outPath = "D:/BigdataProject/data_ML_result"
dest = os.path.join(outPath , 'data', 'pklObject')
pickle.dump(clf , open(os.path.join(dest, 'SVM_1_3.pkl'), 'wb' ), protocol=4)

