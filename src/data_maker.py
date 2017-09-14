# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:13:36 2017

@author: user
"""

from konlpy.tag import Kkma
from nltk import collocations
from collections import Counter
import csv
import os
import pandas as pd
#csv 파일 불러오기


target_dir = os.path.normpath('C:/data') # remove trailing separator.

for fname in os.listdir(target_dir):
    full_dir = os.path.join(target_dir, fname)

    print(full_dir)
    #print(os.path.isdir(full_dir))
    #print(fname[0:-4])
    
    texi_test = pd.read_csv(full_dir,delimiter='$',engine='python',names=['rating','name','text','no'],encoding="utf-8-sig",error_bad_lines=False)
    #리뷰 형태소 분석
        
    rate =[]
    for i in texi_test['rating']:
        rate.append(int(i))
    
    docs=[]
    kkma = Kkma()
    for i in texi_test['text']:
        try:docs.append(kkma.pos(i))
        except:docs.append(' ')  
    
    '''
    #리뷰 연어 분석
    collo=[]
    measure = collocations.BigramAssocMeasures()
    for i in docs:
        finder = collocations.BigramCollocationFinder.from_words(i)
        collo.append(finder.nbest(measure.pmi,5))
       
    
    #영화에 대한 연어 집합 생성
    collo_list = []
    for i in range(len(collo)):
        for j in range(len(collo[i])):
            collo_list.append(collo[i][j])
            
    #연어별 빈도 생성
    count = Counter(collo_list)
    collo_top1000 = count.most_common(1000)
    #collo_top1000[0][0]
    
    #top-1000 연어 집합 생성
    collo_set = [row[0] for row in collo_top1000]
    
    #연어별 점수 생성
    num=0
    collo_score_list=[]
    for col in range(len(collo_set)):
        for i in range(len(collo)):
            if collo_set[col] in collo[i]:
                num += rate[i]
            else:
                num += 0
        avg = num / collo_top1000[col][1]
        collo_score_list.append(avg)
        num = 0
        avg = 0
    #영화 평점 계산
    mean_total = sum(rate[0::]) / len(texi_test)
    #결과 set 생성 (연어, 연어 평균 점수, 영화 점수)
    texi_collo_result = []
    for i in range(len(collo_set)):
        texi_collo_result.append([collo_set[i], collo_score_list[i], mean_total])
    
    #연어 결과 내보내기
    output = "C:/result/" + fname[0:-4] + '.csv'
    
    e = open(output, 'w', encoding="utf-8-sig")
    f = csv.writer(e)
    f.writerows(texi_collo_result)
    e.close()
    '''
    #형태소 집합 생성
    pos_list = []
    for i in range(len(docs)):
        for j in range(len(docs[i])):
            pos_list.append(docs[i][j])           
    #형용사 집합 생성
    va_list=[]
    for i in range(len(pos_list)):
        if pos_list[i] != ' ':
            if pos_list[i][1] == 'VA':
                va_list.append(pos_list[i])            
  
    #top-1000 형용사 집합 생성
    count2 = Counter(va_list)
    va_top1000 = count2.most_common(200)
    va_set = [row[0] for row in va_top1000]
    
    #형용사별 점수 생성
    num=0
    va_score_list=[]
    for v in range(len(va_set)):
        for i in range(len(docs)):
            for j in range(len(docs[i])):
                if va_set[v] == docs[i][j]:
                    num += rate[i]
                else:
                    num += 0
        avg = num / va_top1000[v][1]
        va_score_list.append(avg)
        num = 0
        avg = 0
    
    #영화 평점 계산
    mean_total = sum(rate[0::]) / len(texi_test)
    
    #결과 set 생성 (연어, 연어 평균 점수, 영화 점수)
    texi_va_result = []
    for i in range(len(va_set)):
        texi_va_result.append([va_set[i], va_score_list[i], mean_total])                        
        
    #형용사 결과 내보내기
    output2 = "C:/result/" + fname[0:-4] + '_NN.csv'
    a = open(output2, 'w', encoding="utf-8-sig")
    b = csv.writer(a)
    b.writerows(texi_va_result)
    a.close()
    
    
'''
# TXT file to CSV file
import csv
import os

for fname in os.listdir("C:/txtData"):
    full_dir = os.path.join("C:/txtData", fname)

    print(full_dir)
   # print(os.path.isdir(full_dir))
   # print(fname[0:-4])

    with open(full_dir, "r", encoding="utf-8-sig") as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("$") for line in stripped if line)
        
        path = 'C:/data/'+fname[0:-4]+'.csv'
        with open(path, 'w', encoding="utf-8-sig") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
'''
            
            
            
