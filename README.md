# Demo spark

Testing spark eficiency on a simple scapping + ner case (the most frequent term).

## Usage

To run 6 articles, timing them 5 times, use:

```bash
python run.py -a 6 -n 5
```

To run spark:

```bash
./start-master.sh -h 127.0.0.1
./start-slave.sh spark://127.0.0.1:7077
```