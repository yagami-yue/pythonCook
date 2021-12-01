# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:lesson_1.py
@time:2021/11/05
"""
from nltk.corpus import wordnet as wn

panda = wn.synset('panda.n.01')
hyper = lambda s: s.hypernyms()
print(list(panda.closure(hyper)))
