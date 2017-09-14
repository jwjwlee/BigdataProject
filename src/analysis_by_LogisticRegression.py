# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:48:56 2017

@author: Jungwon Lee
"""

import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from scipy import sparse, io
from sklearn.feature_extraction.text import TfidfVectorizer


train = pd.read_csv('D:/BigdataProject/data_Test_Train_set/train2.csv', encoding='utf-8', engine='python', names=['text','label'])
test = pd.read_csv('C:/Users/user/test.csv', encoding='utf-8', engine='python',names=['text' , 'label'])
train = train.dropna(axis=0)
test = test.dropna(axis=0)

x_train = train['text']
y_train = train['label']
x_test = test['text']
y_test = test['label']


from konlpy.tag import Twitter
twit = Twitter()


twit = Twitter()
def tokenizer(text):
    return twit.morphs(text)


# 벡터화 시키기
vect_1_3 = TfidfVectorizer(ngram_range=(1,5), min_df = 3, 
                               tokenizer=tokenizer).fit(x_train)
nx_train_1_3 = vect_1_3.transform(x_train)
io.mmwrite('nx_train_1_3.mtx', nx_train_1_3)




# 최적옵션 찾기
param_grid_1_3 = {'C' : [1, 10.0, 100.0],'penalty' : ['l1','l2']}

grid_1_3 = GridSearchCV(LogisticRegression(), param_grid_1_3, cv=5) 
grid_1_3.fit(nx_train_1_3,y_train) 

print(grid_1_3.best_score_) #0.8835733333
print(grid_1_3.best_params_) # C : 10 , penalty = 'l2'


# 로지스틱 회귀
lr_grid_1_3 = LogisticRegression(C=10.0, penalty='l2', random_state=10)
lr_grid_1_3.fit(nx_train_1_3, y_train)


#머신러닝 결과 저장
import pickle
curDir = os.getcwd()
dest = os.path.join(curDir , 'data', 'pklObject')
if not os.path.exists(dest):
    os.makedirs(dest)
    
pickle.dump(lr_grid_1_3 , open(os.path.join(dest, 'logit_1_3.pkl'), 'wb' ), protocol=4)

##참고##
#결과 불러오기
logit_1_3 = pickle.load(open(os.path.join(curDir, 'data' , 'pklObject','logit_1_3.pkl'),'rb'))