# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:51:45 2017

@author: user
"""
import re
import csv
import os
import pandas as pd
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]','', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!\-_+<>@\#$%&\\\=\(\'\"ㅋ\ㅜ\ㅠ\ㅎ]', '',
                    cleaned_text)
    return cleaned_text

#영화 리뷰 데이터 하나로 합치기
dir = os.path.normpath('C:/Users/user/Desktop/data')            
for fname in os.listdir(dir):
    full_dir = os.path.join(dir,fname)
    
    print(full_dir)
    
    
    with open(full_dir, "r", encoding="utf-8-sig") as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)

        path = 'C:/Users/user/Desktop/dataset.csv'
        with open(path, 'a', encoding="utf-8-sig") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)

#데이터 불러오기
dataset=[]
dataset = pd.read_csv('C:/Users/user/Desktop/dataset.csv',names=['rating','name','text','blank'],
                      delimiter= '$')
#공백인 리뷰 제거
dataset2=[]
dataset2 = dataset[['rating', 'text']].dropna(axis=0)
dataset3 = dataset2[ dataset2['text'] != ' ' ]
#리뷰에 대해 전처리 수행 (영어 , 특수 문자 등 제거)
dataset4= []
for i in dataset3.index:
    dataset4.append([dataset3.iloc[i][0], clean_text(dataset3.iloc[i][1])])
#결과 내보내기
a = open('dataset4.csv', 'w' , encoding='utf-8-sig')
b = csv.writer(a)
b.writerows(dataset4)
a.close()      
