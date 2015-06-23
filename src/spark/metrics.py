#Wordcount program with word rate per batch size and other mertrics
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import sys
import time


conf = SparkConf()
conf.setMaster("local")
conf.setAppName("WordCount")
conf.set("spark.executor.memory", "1g")

batch_size = 2
countrate = 0
#start = time.time()


def wordRate(l,seconds):

    word_pairs = l.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word,1))

    number_pairs = word_pairs.count()
    word_rate = number_pairs.map(lambda x: (float(x) / seconds))
    word_rate.pprint()



if __name__ == "__main__":


    sc = SparkContext(appName="WordCount")
    ssc = StreamingContext(sc, int(batch_size))
    zkQuorum = "public-ip:2181,public-ip:2181,public-ip:2181,public-ip:2181"
    #zkQuorum = "public-ip:2181"

    kvs = KafkaUtils.createStream(ssc,zkQuorum,"consumer-random",{"random_words": 1} )
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)


    #end = time.time()
    #time_diff = end - start

    counts.pprint()
    wordRate(lines,batch_size)   


    #end = time.time()
    #time_diff = end - start

    ssc.start()
    ssc.awaitTermination()