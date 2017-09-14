# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:39:07 2017

@author: user
"""

from soynlp.word import WordExtractor


class Sentences:
    def __init__(self, fname):
        self.fname = fname
        self.length = 0
    def __iter__(self):
        with open(self.fname, encoding='utf-8') as f:
            for doc in f:
                doc = doc.strip()
                if not doc:
                    continue
                for sent in doc.split('  '):
                    yield sent
    def __len__(self):
        if self.length == 0:
            with open(self.fname, encoding='utf-8') as f:
                for doc in f:
                    doc = doc.strip()
                    if not doc:
                        continue
                    self.length += len(doc.split('  '))
        return self.length

def read_data(filename):
    with open(filename, 'r' , encoding='utf-8-sig') as f:
        data = [line.split('$') for line in f.read().splitlines()]
    return data

def word_score(score):
    import math
    return (score.cohesion_forward * math.exp(score.right_branching_entropy))


#Test  
from konlpy.tag import Twitter
twit = Twitter()

def tokenizer2(text):
    return twit.morphs(text) 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import re
import os
import pandas as pd

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]','', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!\-_+<>@\#$%&\\\=\(\'\"ㅋ\ㅜ\ㅠ\ㅎ]', '',
                    cleaned_text)
    return cleaned_text

dataset4 = read_data('D:/BigdataProject/data_Review/장산범_cleand.txt')

dataset5 = [(dataset4[x][0], clean_text(dataset4[x][2]).strip()) for x in range(len(dataset4)) ]

택시운전사 = [(dataset5[x][0], dataset5[x][1]) for x in range(len(dataset5)) if len(dataset5[x][1])  >= 1 ]



postaxi = pd.DataFrame([(row[1] , 1 ) for row in 택시운전사 if int(row[0]) >=9] , columns=['text','label'])
negtaxi = pd.DataFrame([(row[1] , 0 ) for row in 택시운전사 if int(row[0]) <=4] , columns=['text','label'])
taxi = pd.concat([postaxi, negtaxi] ,axis=0)
x_taxi = taxi['text']
y_taxi = taxi['label']
train = pd.read_csv('C:/Users/HyunJin/train.csv', encoding='utf-8', engine='python', names=['text','label'])
train = train.dropna(axis=0)

x_train = train['text']
vect_5_3 = TfidfVectorizer(ngram_range=(1,5), min_df = 3, tokenizer=tokenizer2).fit(x_train)
nx_taxi_5_3 = vect_5_3.transform(x_taxi)


import pickle
curDir = os.getcwd()

logit_5_3 = pickle.load(open(os.path.join(curDir, 'data' , 'pklObject','logit_5_3.pkl'),'rb'))

y_pred = logit_5_3.predict(nx_taxi_5_3)
print('정확도:' , accuracy_score(y_taxi,y_pred))





pos_taxi_re = []
neg_taxi_re = []
for i in range(len(x_taxi)):
    if y_pred[i] == 1:
        pos_taxi_re.append(x_taxi.iloc[i])
    elif y_pred[i] == 0:
        neg_taxi_re.append(x_taxi.iloc[i])


from soynlp.word import WordExtractor


#긍정키워드
pos_taxi_re1  =pd.DataFrame(pos_taxi_re)
pos_taxi_re1.to_csv('pos_taxi_re.csv', index=False, header=False, encoding = 'utf-8-sig')  
corpus_fname = 'C:/Users/HyunJin/pos_taxi_re.csv'
sentences = Sentences(corpus_fname)

word_extractor = WordExtractor(min_count=150,
                               min_cohesion_forward=0.5, 
                               min_right_branching_entropy=0.0)

word_extractor.train(sentences)
words = word_extractor.extract()


print('단어   (빈도수, cohesion, branching entropy)\n')
posword = []
for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:10]:
    if len(word) > 1 and  score.right_branching_entropy > 1:
        print('%s     (%d, %.3f, %.3f)' % (word, 
                                   score.leftside_frequency, 
                                   score.cohesion_forward,
                                   score.right_branching_entropy
                                  ))
        posword.append([word,score.leftside_frequency])
        
posword
    
#부정키워드    
neg_taxi_re1  =pd.DataFrame(neg_taxi_re)
neg_taxi_re1.to_csv('neg_taxi_re.csv', index=False, header=False, encoding = 'utf-8-sig')  
corpus_fname = 'C:/Users/HyunJin/neg_taxi_re.csv'
sentences = Sentences(corpus_fname)

word_extractor = WordExtractor(min_count=10,
                               min_cohesion_forward=0.5, 
                               min_right_branching_entropy=0.0)

word_extractor.train(sentences)
words = word_extractor.extract()


print('단어   (빈도수, cohesion, branching entropy)\n')
negword=[]
for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:20]:
    print('%s     (%d, %.3f, %.3f)' % (word, 
                                   score.leftside_frequency, 
                                   score.cohesion_forward,
                                   score.right_branching_entropy
                                  ))


    negword.append([word,score.leftside_frequency])

    
    
#긍정 추출 함수
def testFuction1(keyword):
    역사= []
    for i in pos_taxi_re:
        if keyword in i:
           역사.append(i) 
    역사1  =pd.DataFrame(역사)
    역사1.to_csv(keyword+'.csv', index=False, header=False, encoding = 'utf-8-sig')  
    corpus_fname = 'C:/Users/HyunJin/'+keyword+'.csv'
    sentences = Sentences(corpus_fname)
    
    word_extractor = WordExtractor(min_count=1,
                                   min_cohesion_forward=0, 
                                   min_right_branching_entropy=0.0)
    
    word_extractor.train(sentences)
    words = word_extractor.extract()
    
    
    print('단어   (빈도수, cohesion, branching entropy)\n')
    역사_word=[]
    for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:20]:
        if len(word) >1:
            print('%s     (%d, %.3f, %.3f)' % (word, 
                                           score.leftside_frequency, 
                                           score.cohesion_forward,
                                           score.right_branching_entropy
                                          ))
        역사_word.append([word,score.leftside_frequency])
    
    from konlpy.tag import Kkma
    kkma = Kkma()
    
    역사_noun = [(kkma.nouns(row[0]), row[1]) for row in 역사_word]
    
    
    역사_noun2 = []
    for i in range(len(역사_noun)):
        for j in range(len(역사_noun[i][0])):
            if len(역사_noun[i][0][j]) >1:
                역사_noun2.append([역사_noun[i][0][j], 역사_noun[i][1]])
       
    역사_noun_set = list(set([row[0] for row in 역사_noun2]))
    
    cnt = 0
    역사_noun_re = []
    for i in 역사_noun_set:
        for j in range(len(역사_noun2)):
            if i ==  str(역사_noun2[j][0]):
                cnt += 역사_noun2[j][1]    
        역사_noun_re.append([i, cnt])
        cnt= 0
                

    역사_noun_re  =pd.DataFrame(역사_noun_re)
    역사_noun_re.to_csv('pos_'+keyword+'noun_re.csv', index=False, header=False, encoding = 'utf-8-sig') 

#부정 추출 함수
def testFuction2(keyword):
    역사= []
    for i in neg_taxi_re:
        if keyword in i:
           역사.append(i) 
    역사1  =pd.DataFrame(역사)
    역사1.to_csv(keyword+'.csv', index=False, header=False, encoding = 'utf-8-sig')  
    corpus_fname = 'C:/Users/HyunJin/'+keyword+'.csv'
    sentences = Sentences(corpus_fname)
    
    word_extractor = WordExtractor(min_count=1,
                                   min_cohesion_forward=0, 
                                   min_right_branching_entropy=0.0)
    
    word_extractor.train(sentences)
    words = word_extractor.extract()
    
    
    print('단어   (빈도수, cohesion, branching entropy)\n')
    역사_word=[]
    for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:20]:
        if len(word) >1:
            print('%s     (%d, %.3f, %.3f)' % (word, 
                                           score.leftside_frequency, 
                                           score.cohesion_forward,
                                           score.right_branching_entropy
                                          ))
        역사_word.append([word, score.leftside_frequency])
    
    from konlpy.tag import Kkma
    kkma = Kkma()
    
    역사_noun = [(kkma.nouns(row[0]), row[1]) for row in 역사_word]
    
    
    역사_noun2 = []
    for i in range(len(역사_noun)):
        for j in range(len(역사_noun[i][0])):
            if len(역사_noun[i][0][j]) >1:
                역사_noun2.append([역사_noun[i][0][j], 역사_noun[i][1]])
            
            
        
    역사_noun_set = list(set([row[0] for row in 역사_noun2]))
    
    cnt = 0
    역사_noun_re = []
    for i in 역사_noun_set:
        for j in range(len(역사_noun2)):
            if i ==  str(역사_noun2[j][0]):
                cnt += 역사_noun2[j][1]    
        역사_noun_re.append([i, cnt])
        cnt= 0
                
                  
    역사_noun_re  =pd.DataFrame(역사_noun_re)
    역사_noun_re.to_csv('neg_'+keyword+'_noun_re.csv', index=False, header=False, encoding = 'utf-8-sig') 


for keyword in range(len(posword)):
    testFuction1(posword[keyword][0])

for keyword in range(len(negword)):
    testFuction2(negword[keyword][0])