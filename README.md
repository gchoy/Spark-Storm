#Testing Spark Streaming and Storm



#Table of Contents
- <a href= "https://github.com/gchoy/Spark-Storm/blob/master/README.md#introduction">Introduction</a>
- <a href= "https://github.com/gchoy/Spark-Storm/blob/master/README.md#testing-setup">Testing Setup</a>
- <a href= "https://github.com/gchoy/Spark-Storm/blob/master/README.md#data">Data</a>
- <a href= "https://github.com/gchoy/Spark-Storm/blob/master/README.md#presentation">Presentation</a>
- <a href= "https://github.com/gchoy/Spark-Storm/blob/master/README.md#instructions-to-setup-this-pipline">Instructions to Set up this Pipeline</a>

#Introduction
In this data engineering project we tested two processing frameworks: Spark streaming and Storm. The two main goals were:
- To understand the differences between Spark Streaming and Storm.
- Test the processing frameworks under different loads and measure throughput.

#Testing Setup
- **Testing Conditions:** Each framework was set in separate clusters of 4 nodes on AWS.
- **Metrics that were measured:** Amount of data processed / records per second (throughput).
- **Time:** Tests were run for aproximately 10 minutes in both pipelines.
- **Caveat:** The results obtained must be taken with precaution due to processing and semantic differences between Spark streaming and Storm.     

<img src="https://github.com/gchoy/Spark-Storm/blob/master/images/pipeline.png" style="width:304px;height:228px;">

<img src="https://github.com/gchoy/Spark-Storm/blob/master/images/specs.png" style="width:304px;height:228px;">
  
#Data 
The data was generated by a producer that selected words from a list and created a comma separated string which was streamed through Kafka to a consumers in Spark/Storm.

#Use case
Word count is a often a popular choice when testing frameworks.
Other uses cases that I would like to implement would be a sorting algorithm and/or a graph.

#Cluster Setup
Two distributed AWS clusters of four ec2 m3.medium nodes were used. The  ingestion components, and processing frameworks were configured and run in distributed mode, with one master and three workers for Spark streaming, and one nimbus and three supervisors for Storm.

#Instructions to Set up this Pipeline

- Spin 4 ec2 nodes, install Hadoop, Zookeeper, Kafka, Spark, and Storm 

- Start Zookeeper and Kafka

- Select which processing framework you want to test, and start it.

- Install python packages:
```sudo pip install kafka-python```

- Run the Kafka producer using the bash script:
```python spark/producer.py```

- Run pyspark script:
```$SPARK_HOME/bin/spark-submit metrics.py```

**Or:**

- Install python packages:
```sudo pip install pyleus ```

- Build storm topology:
```pyleus build word_topology.yaml```

- Test the topology by running it locally
```pyleus local word_topology.jar -d```

- Submit pyleus topology:
```pyleus submit -n  <public-dns> word_topology.jar```

**Note:** Zookeeper and Kafka must be running before starting the producer, or metrics.py or submiting the Storm topology.

#Presentation 
The presentation slides are available here:
<a href= "https://gchoy.github.io/index.html">gchoy.github.io</a>

