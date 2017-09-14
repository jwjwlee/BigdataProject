# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:09:34 2017

@author: user
"""

import pandas as pd
import scipy as sp
movie = pd.read_csv('C:/Users/user/Desktop/프로젝트/movie.csv', engine='python')
pos = pd.read_csv('C:/Users/user/Desktop/프로젝트/pos.csv', engine='python')
tdist= pd.read_csv('C:/Users/user/Desktop/프로젝트/tdist.csv', engine='python')

#등분산성 검정    
evar =[]
for i in range(len(movie)):
    levene = sp.stats.levene(pos.iloc[i], movie.iloc[i])
    evar.append([levene.statistic,levene.pvalue])
evar_bool=[]    
for i in range(len(evar)):
    if evar[i][1] >  0.05:
        evar_bool.append(True)
    else:
        evar_bool.append(False)
        
#대응표본 t 검정        
result=[]
for i in range(len(movie)):
    ttest = sp.stats.ttest_ind(pos.iloc[i], movie.iloc[i], equal_var=evar_bool[i])
    dist = tdist.iloc[len(pos.iloc[i])-2]
    result.append([ttest.statistic,ttest.pvalue,dist.tstat])

for i in range(len(result)):
    if result[i][1] <= 0.05:
        if result[i][0] > result[i][2]:
            result[i].append("Postive")
        else:
            result[i].append("Negative")
    else:
        result[i].append("NEUT")