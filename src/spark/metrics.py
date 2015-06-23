#Wordcount program with word rate per batch size and other mertrics
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
import sys
import time



conf = SparkConf()
conf.setMaster("local")
conf.setAppName("WordCount")
conf.set("spark.executor.memory", "1g")

batch_size = 2
countrate = 0
#start = time.time()


def wordRate(l):

    word_counts = l.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word,1)).count()

    word_rate = word_counts.map(lambda (x,y): (float(y) / int(batch_size)))
        #.map(lambda word: (word,1)) \
        #.map(lambda (x, y): (float(y) / int(batch_size))).collect()
    return word_rate

    #return individualRate.pprint()
    #return cnts/2


if __name__ == "__main__":


    sc = SparkContext(appName="WordCount")
    ssc = StreamingContext(sc, int(batch_size))
    #zkQuorum = "52.8.175.21:2181,52.8.178.31:2181,52.8.149.129:2181,52.8.177.10:2181"
    zkQuorum = "52.8.175.21:2181"

    kvs = KafkaUtils.createStream(ssc,zkQuorum,"consumer-random",{"random_words": 1} )
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)


    #end = time.time()
    #time_diff = end - start

