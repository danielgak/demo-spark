# Demo spark

Simple test for spark eficiency on a scapping + nlp case. It downloads the same a articles and process them n times. There are 3 difierent aproximations, and all of them return the most frequent terms.

## Dependencies

BeautifulSoup, Pyspark, nltk, java 1.8 and python 3.7

## Usage

To run 6 articles, timing them 5 times, use:

```bash
python run.py -a 50 -n 2
```

To run spark:

```bash
./start-master.sh -h 127.0.0.1
./start-slave.sh spark://127.0.0.1:7077
```

Output example:

```bash
$> python run.py -a 100 -n 2
Result 100 articles, 2 iterations:
	Equal results: False
	Result: 	 [('division', 104), ('paris', 99), ('league', 86), ('fire', 84), ('moths', 73), ('\\xe2\\x80\\x93', 73), ('mcadoo', 71), (']', 68), ('wrl', 64), ('empire', 60)]
	Result 1: 	 [('division', 104), ('paris', 99), ('league', 86), ('fire', 84), ('moths', 73), ('\\xe2\\x80\\x93', 73), ('mcadoo', 71), (']', 68), ('wrl', 64), ('season', 60)]
	Result 2: 	 [(']', 545), ('city', 180), ('articles', 166), ('fire', 130), ('site', 126), ('division', 120), ('league', 118), ('links', 115), ('page', 114), ('commons', 113)]

Timing:
	Base: 	 	 25.215457133
	Case 1: 	 16.32577133000001
	Case 2: 	 42.67574317200001
```

## Conclusions:

Stil we could make some changes (the terms aren't perfect tokenized, etc), but the conclusion is quite simple:

- The base script gives the only the top 10 most frecuent terms for each article, and from those top10 the script returns the top 10 of the whole set. (~ 12 seconds)
- The case1 is a modification of the base script so it uses spark to paralellize the nlp process of each article. With a simple cluster in my local machine, it's two times faster with 100 articles. (~ 7 seconds)
- The case2 it's a case, when instead of taking only the top 10 most frecuent term, we calculate the set over all. Surprisingly, for all the aditional computation, it only doubles the time, giving a complete result. (~ 21 seconds)

