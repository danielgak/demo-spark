# Standard library imports
import requests
import itertools
import operator
import functools

# Local application imports

# Third party imports
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from bs4 import BeautifulSoup

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

def case1_wiki_ner(articles):
    top = []
    for html in articles:
        tokens = preprocess(str(html).replace('[','').replace(']',''))
        nouns = filter(lambda x: 'NN' in x[1],tokens)
        weighted = map(lambda x: (x[0],1),nouns)
        frecuency = accumulate(weighted)
        s = sorted(frecuency,key=operator.itemgetter(1),reverse=True)
        top = s[:10] + top[:]
    top = sorted(top,key=operator.itemgetter(1),reverse=True)
    return top[:10]