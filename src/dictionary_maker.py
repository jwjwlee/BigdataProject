# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 16:44:57 2017

@author: Jungwon Lee
"""

import csv
import os
import pandas as pd


dir = os.path.normpath('C:/COL_DATA/')
#데이터 불러오기
for fname in os.listdir(dir):
    full_dir = os.path.join(dir,fname)
    
    print(full_dir)
    
    
    with open(full_dir, "r", encoding="utf-8-sig") as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        
        path = 'C:/Result/result_collo.csv'
        with open(path, 'a', encoding="utf-8-sig") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
            
            
result_collo=[]
result_collo = pd.read_csv('C:/Result/result_collo.csv',names=['a','b','c','d','score','total'])

#연어, 합치기
colloset=[]
for i in range(len(result_collo)):
    colloset.append([result_collo.iloc[i][0] +"," +result_collo.iloc[i][1] + ' ' 
                     + result_collo.iloc[i][2] +"," +result_collo.iloc[i][3], 
                     result_collo.iloc[i][4], result_collo.iloc[i][5] ])

#연어 집합 생성    
colloset2=[]
for i in range(len(colloset)):
    colloset2.append(colloset[i][0])
colloset3 = list(set(colloset2))

colloset4=[]
colloset4=[[i] for i in colloset3]
for i in range(len(colloset3)):
    for j in range(len(colloset)):
        if colloset3[i] == colloset[j][0]:
            colloset4[i].append([colloset[j][1],colloset[j][2]])

#대응 표본 생성
x=[[i] for i in colloset3]
y=[[i] for i in colloset3]

for i in range(len(colloset4)):
    for j in range(1,len(colloset4[i])):
        x[i].append(colloset4[i][j][0])
        y[i].append(colloset4[i][j][1])

samplelen = []
for i in range(len(x)):
    samplelen.append(len(x[i]))

samplelen2 = sorted(samplelen , reverse=True)

import matplotlib.pyplot as plt
index = [int(i) for i in range(len(samplelen2))]
plt.bar(index,samplelen2)

import scipy.stats 
import scipy as sp

#일정 이상 표본만 생성
nx=[]
ny=[]
for i in range(len(x)):
    if len(x[i]) >=101 :
        nx.append(x[i])
        ny.append(y[i])

#등분산성 검정   
evar =[]
for i in range(len(nx)):
        levene = sp.stats.levene(nx[i][1::], ny[i][1::])
        evar.append([levene.statistic,levene.pvalue])
evar_bool=[]    
for i in range(len(evar)):
    if evar[i][1] >  0.05:
        evar_bool.append(True)
    else:
        evar_bool.append(False)
        
#대응표본 t 검정        
tdist= pd.read_csv('C:/data/tdist.csv', engine='python')
result=[]
for i in range(len(nx)):
    ttest = sp.stats.ttest_ind(nx[i][1::], ny[i][1::], equal_var=evar_bool[i])
    dist = tdist.iloc[len(nx[i][1::])-2]
    result.append([nx[i][0],ttest.statistic,ttest.pvalue,dist.tstat])

for i in range(len(result)):
    if result[i][2] <= 0.05:
        if result[i][1] > result[i][3]:
            result[i].append("Postive")
        else:
            result[i].append("Negative")
    else:
        result[i].append("Neutral")
        
        
        
output = open('C:/data/result_collo_set(100).csv', 'w')
b = csv.writer(output)
b.writerows(result)
output.close()

