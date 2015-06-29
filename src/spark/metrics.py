from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from operator import add
from uuid import uuid1
import sys
import time


conf = SparkConf()
conf.setMaster("local")
conf.setAppName("WordCount")
conf.set("spark.executor.memory", "1g")

batch_size = 1
countrate = 0


def wordRate(l,seconds):
    
    """Calculates the record per second and throughput
       and stamps the time"""
    
    word_pairs = l.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word,1))

    number_pairs = word_pairs.count()
    time_stamp = time.time()

    stamped_total = number_pairs.map(lambda x: (x, time_stamp))
    stamped_total.pprint()
    
    word_rate = number_pairs.map(lambda x: (float(x) / seconds))
    #word_rate.pprint()
    stamped_rate = word_rate.map(lambda x: (x, time_stamp))
    stamped_rate.pprint()   


if __name__ == "__main__":
    
      
    sc = SparkContext(appName="WordCount")
    ssc = StreamingContext(sc, int(batch_size))
    zkQuorum = "52.8.175.21:2181,52.8.178.31:2181,52.8.149.129:2181,52.8.177.10:2181"
    #zkQuorum = "52.8.175.21:2181"

    kvs = KafkaUtils.createStream(ssc,zkQuorum,"consumer-random",{"random_words": 1} )
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(",")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    

    counts.pprint()
    wordRate(lines,batch_size)
    
      
    ssc.start()
    ssc.awaitTermination()

