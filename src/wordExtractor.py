# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:07:01 2017

@author: Jungwon Lee
"""


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

옥자 = read_data('D:/BigdataProject/data_Review/옥자_cleand.txt')


옥자2 = [옥자[x][2] for x in range(len(옥자)) ]
print(옥자2)

import csv

path = "okja.csv"

with open(path, 'w', encoding="utf-8-sig") as out_file:
    writer = csv.writer(out_file)
    writer.writerows(옥자2)




corpus_fname = 'okja.csv'
sentences = Sentences(corpus_fname)
print('num sentences = %d' % len(sentences))




from soynlp.word import WordExtractor

word_extractor = WordExtractor(min_count=100,
                               min_cohesion_forward=0.05, 
                               min_right_branching_entropy=0.0)

word_extractor.train(sentences)
words = word_extractor.extract()




def word_score(score):
    import math
    return (score.cohesion_forward * math.exp(score.right_branching_entropy))

print('단어   (빈도수, cohesion, branching entropy)\n')
for word, score in sorted(words.items(), key=lambda x:word_score(x[1]), reverse=True)[:30]:
    print('%s     (%d, %.3f, %.3f)' % (word, 
                                   score.leftside_frequency, 
                                   score.cohesion_forward,
                                   score.right_branching_entropy
                                  ))



