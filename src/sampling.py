# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 21:39:16 2017

@author: user
"""


import re
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
def read_data(filename):
    with open(filename, 'r' , encoding='utf-8-sig') as f:
        data = [line.split(',') for line in f.read().splitlines()]
    return data
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]','', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!\-_+<>@\#$%&\\\=\(\'\"ㅋ\ㅜ\ㅠ\ㅎ]', '',
                    cleaned_text)
    return cleaned_text
#데이터 전처리
dataset4 = read_data('C:/Users/user/Desktop/dataset4.csv')

dataset5 = [(dataset4[x][0], clean_text(dataset4[x][1])) for x in range(len(dataset4)) if x % 2 == 0 ]

dataset6 = [(dataset5[x][0], dataset5[x][1].strip()) for x in range(len(dataset5)) ]

for i in range(len(dataset6)):
    if len(dataset6[i][1]) < 1:
        print(dataset6[i][1])
dataset7 = [(dataset6[x][0], dataset6[x][1]) for x in range(len(dataset6)) if len(dataset6[x][1])  >= 1 ]

# 전처리 결과 내보내기
c = open('C:/Users/user/Desktop/dataset6.csv', 'w', encoding ='utf-8-sig')
d = csv.writer(c)
d.writerows(dataset6)
c.close()

#평점 9~10 : 긍정 리뷰(1) , 평점 1~4 : 부정 리뷰(0) 로 분리
posdataset = pd.DataFrame([(row[1] , 1 ) for row in dataset7 if int(row[0]) >=9] , columns=['text','label'])
negdataset = pd.DataFrame([(row[1] , 0 ) for row in dataset7 if int(row[0]) <=4] , columns=['text','label'])

#분리된 셋에서 100000개 씩 표본 추출
possample = pd.DataFrame(posdataset).sample(n=100000, random_state=10)
negsample = pd.DataFrame(negdataset).sample(n=100000, random_state=10)

#Train , Test set으로 나누기
pos_train, pos_test = train_test_split(possample, random_state=10)
neg_train, neg_test = train_test_split(negsample, random_state=10)
train =pd.concat([pos_train, neg_train], axis = 0)
test =pd.concat([pos_test, neg_test], axis = 0)

#결과 내보내기
train.to_csv('C:/Users/user/train.csv', na_rep='NaN', index=False, encoding='utf-8-sig')
test.to_csv('C:/Users/user/test.csv',  na_rep='NaN', index=False, encoding='utf-8-sig')

