# Standard library imports
import os
import argparse
import requests
import timeit

# Third party imports
from pyspark import SparkContext

# Local application imports
from src.base import base_wiki_ner
from src.case1 import case1_wiki_ner
from src.case2 import case2_wiki_ner

def _wikipedia_pages_generator(n: int):
    for _ in range(0,n):
        yield requests.get("http://en.wikipedia.org/wiki/Special:Random").content
        # yield "Good muffins cost $3.88\nin New York. Please buy me. I wrote a test with two of them.\n\nThanks. The test was good."

parser = argparse.ArgumentParser(description='Full upload, or continue uploading')
parser.add_argument('--articles', '-a', dest='a', type=int)
parser.add_argument('--n', '-n', dest='n', type=int)
args = parser.parse_args()

if(args.a is None or args.a < 1):
    args.a = 1

if(args.n is None or args.n < 1):
    args.n = 1

# We download the articles so the conection or diferent lenghts don`t affect
articles = list(_wikipedia_pages_generator(args.a))

# Spark context
sc = SparkContext.getOrCreate()

res = base_wiki_ner(articles)
res1 = case1_wiki_ner(articles,sc)
res2 = case2_wiki_ner(articles,sc)

t = timeit.timeit("base_wiki_ner(articles)", globals=globals(), number=args.n)
t1 = timeit.timeit("case1_wiki_ner(articles,sc)", globals=globals(), number=args.n)
t2 = timeit.timeit("case2_wiki_ner(articles,sc)", globals=globals(), number=args.n)

print("Result {} articles, {} iterations: \n\
\tEqual results: {}\n\
\tResult: \t {}\n\
\tResult 1: \t {}\n\
\tResult 2: \t {}\n\
\n\
Timing:\n\
\tBase: \t \t {}\n\
\tCase 1: \t {}\n\
\tCase 2: \t {}\n".format(args.a, args.n, res == res1 == res2, res, res1, res2, t, t1, t2))
