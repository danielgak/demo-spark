# Standard library imports
import requests
import itertools
import operator
import functools

# Third party imports
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from bs4 import BeautifulSoup
from pyspark import SparkContext


def _clean_tags(text):
    soup =  BeautifulSoup(text, features="lxml")
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text(strip=True)

def preprocess(html: str):
    text = _clean_tags(html.lower())
    tokenized  = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenized)
    return tagged

def accumulate(l):
    s = sorted(l,key=operator.itemgetter(0))
    it = itertools.groupby(s, operator.itemgetter(0))
    for key, subiter in it:
        yield key, sum(item[1] for item in subiter)

def _wiki_ner(article):
    tokens = preprocess(str(article).replace('[','').replace(']',''))
    nouns = filter(lambda x: 'NN' in x[1],tokens)
    weighted = map(lambda x: (x[0],1),nouns)
    frecuency = accumulate(weighted)
    return sorted(frecuency,key=operator.itemgetter(1),reverse=True)[:10]

def case1_wiki_ner(articles,sc: SparkContext):
    results = sc.parallelize(articles).map(_wiki_ner).collect()
    top = []
    for res in results:
        top += res[:]
    top = sorted(top,key=operator.itemgetter(1),reverse=True)
    return top[:10]