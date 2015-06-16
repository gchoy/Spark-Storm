from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
import sys




conf = SparkConf()
conf.setMaster("local")
conf.setAppName("WordCount")
conf.set("spark.executor.memory", "1g")
#sc = SparkContext(conf = conf)


if __name__ == "__main__":
    #if len(sys.argv) != 3:
    #    print >> sys.stderr, "Usage: "
    #    exit(-1)


    sc = SparkContext(appName="WordCount")
    ssc = StreamingContext(sc, 2)
    #zkQuorum = ("public-dns:2181","public-dns:2181","public-dns:2181","public-dns:2181")
    zkQuorum = "public dns:2181"

    #brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc,zkQuorum,"consumer-random",{"random_words": 1} )
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
