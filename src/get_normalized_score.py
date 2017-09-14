# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:50:13 2017

@author: Jungwon Lee
"""

import csv
import os
import pandas as pd

# 감성 사전 불러오기
sentiment_value = pd.read_csv("D:/BigdataProject/sentiment_Dictionary/collo_positive.csv",delimiter=',',
                              engine='python', names=['word', 'ttest', 'pvalue', 'dist', 'polar'])

# (최대,최소)차이 값 계산
gap = sentiment_value['ttest'] - sentiment_value['dist']
maxGap = max(gap)
minGap = min(gap)

# 정규
normalizationGap = []
for curValue in gap:
    normalizationGap.append(str((curValue - minGap) / (maxGap - minGap)))
   
# 정규화된 점수 추가     
normalized_result = sentiment_value.join(pd.DataFrame(list(normalizationGap)))
normalized_result.columns.values[5] = 'normalized_value'    

# 정규화 점수가 추가된 data만들기
path = "D:/BigdataProject/sentiment_Dictionary/collo_positive_normalized.csv"
outfile = open(path, 'wb')
normalized_result.to_csv(path, index=False)
outfile.close()   
    
    
    
    
    
    
    
    
    
    
    
    
