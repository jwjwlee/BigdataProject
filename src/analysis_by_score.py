# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 15:35:16 2017

@author: Jungwon Lee
"""

from konlpy.tag import Kkma
from nltk import collocations
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os

# 리뷰 가져오기 
review_data = pd.read_csv("D:/BigdataProject/temp/기술자들_cleand.txt", delimiter='$',
                          engine='python',names=['rating','title','review','no'],
                          encoding="utf-8-sig", error_bad_lines=False)

# 감성 사전 불러오기
collo_positive = pd.read_csv("D:/BigdataProject/sentiment_Dictionary/collo_positive_normalized.csv",delimiter=',',
                              engine='python', names=['word', 'ttest', 'pvalue', 'dist', 'polar', 'norm'])

collo_negative = pd.read_csv("D:/BigdataProject/sentiment_Dictionary/collo_negative_normalized.csv",delimiter=',',
                              engine='python', names=['word', 'ttest', 'pvalue', 'dist', 'polar', 'norm'])

va_positive = pd.read_csv("D:/BigdataProject/sentiment_Dictionary/va_positive_normalized.csv",delimiter=',',
                              engine='python', names=['word', 'ttest', 'pvalue', 'dist', 'polar', 'norm'])

va_negative = pd.read_csv("D:/BigdataProject/sentiment_Dictionary/va_negative_normalized.csv",delimiter=',',
                              engine='python', names=['word', 'ttest', 'pvalue', 'dist', 'polar', 'norm'])


# 리뷰 데이터에서 특정 평점 리뷰만 가져오기
review_data = review_data[(review_data['rating'] > 8) | (review_data['rating'] < 5)]


# 리뷰 형태소 분석
res=[]
kkma = Kkma()
for i in review_data['review']:
    try:
        res.append(kkma.pos(i))
    except:
        res.append('')
        
# 형태소 분석 결과 중 형용사만가져오기(1 row 1 review) 
va=[]
for k in range(0, len(res)):
    temp=[]
    for i in range(0, len(res[k])):
        for j in range(0, 2):
            if res[k][i][j] == 'VA':
                temp.append(res[k][i])
    temp = list(set(temp)) #중복제거
    va.append(temp)


# 리뷰 형용사와 사전 형용사 비교/계산
# 1 row 1 review score
scoreSet=[]
countSet=[]
for k in range(0, len(va)):        
    score = 0
    countSet.append((0))
    for i in range(0, len(va_positive['word'])):
        for j in range(0, len(va[k])):
            if str(va_positive['word'][i][1:-1]) == str(va[k][j]):
                score += float(va_positive['norm'][i])
                countSet[k] += 1
                
    for i in range(0, len(va_negative['word'])):
        for j in range(0, len(va[k])):
            if str(va_negative['word'][i][1:-1]) == str(va[k][j]):
                score += float(va_negative['norm'][i])
                countSet[k] += 1
                
    scoreSet.append(score)


# 리뷰 연어 분석
collo=[]
measure = collocations.BigramAssocMeasures()
for i in res:
    finder = collocations.BigramCollocationFinder.from_words(i)
    collo.append(finder.nbest(measure.pmi,30))
   

# 리뷰 연어와 사전 연어비교/계산  
for k in range(0, len(collo)):        
    for i in range(0, len(collo_positive['word'])):
        for j in range(0, len(collo[k])):
            resCollo = str(collo[k][j][0]) + "  " + str(collo[k][j][1])        
            if collo_positive['word'][i][2:-2] == resCollo:
                scoreSet[k] += float(collo_positive['norm'][i])
                countSet[k] += 1
                
    for i in range(0, len(collo_negative['word'])):
        for j in range(0, len(collo[k])):
            resCollo = str(collo[k][j][0]) + "  " + str(collo[k][j][1])
            if collo_negative['word'][i][2:-2] == resCollo:
                scoreSet[k] += float(collo_negative['norm'][i])
                countSet[k] += 1


#점수로 예측 평점계산
predict = []
for k in range(0, len(res)):
    if scoreSet[k] != 0 and countSet[k] != 0:
        predict.append(int(scoreSet[k] / countSet[k] * 10))
    else:
        predict.append(0)


# 분포
plt.plot(predict)
plt.hist(predict, bins=15)
plt.show()
