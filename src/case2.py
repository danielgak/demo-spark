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
    html = str(html).replace('[','').replace(']','')
    text = _clean_tags(html.lower())
    tokenized  = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokenized)
    return tagged

def accumulate(l):
    s = sorted(l,key=operator.itemgetter(0))
    it = itertools.groupby(s, operator.itemgetter(0))
    for key, subiter in it:
        yield key, sum(item[1] for item in subiter)


def case2_wiki_ner(articles,sc: SparkContext):
    results = sc.parallelize(articles).map(preprocess).flatMap(lambda x: x).filter(lambda x: 'NN' in x[1]).map(lambda x: (x[0],1)).sortBy(lambda x: x[0]).collect()
    # for res in results:
    #     top+=res[:]
    # top = sorted(top,key=operator.itemgetter(1),reverse=True)

    return sorted(accumulate(results),key=operator.itemgetter(1),reverse=True)[:10]