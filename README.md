# Streaming with Pulsar into Astra and Elasticsearch

This proof of concept outlines the steps required to create a data streaming environment using Apache Pulsar Sinks in docker. The implementation uses Pulsar sink connectors to integrate multiple database technologies with data producers without custom coding.

## Use case

A Python client consumes telemetry data from the National weather service APIs. This data should be saved into Astra for low-latency transactions and saved into Elasticsearch for analytics and search. Additional business requirements for this use case may include:

1.  Integration effort with other database technologies should be minimized.

2.  Data streaming platform should be scalable and cost-effective.

## Main Challenges

1.  Clients require low-latency weather telemetry data that could be used for critical weather-dependent services such as aviation and maritime vessels. DataStax Astra is a         great use case for this.

2.  The client requires the ability to run analytics reporting and searches. Elasticsearch will be used for this.

## Why Data Streaming?

Data Streaming platforms simplify handling messages and integrating disparate systems that otherwise would require custom connectors and data integration processes.

**Figure 1** exemplifies a scenario in which multiple weather measuring
technologies developed by different vendors (IBM, Microsoft, Oracle,
etc) produce data to be stored in multiple destination databases and the
number of integrations and complexity required to manage direct
messaging across these systems.

![image](https://user-images.githubusercontent.com/80357022/113936550-e8803580-97c5-11eb-9997-4afeafd3282c.png)
  --------------------------------------------------------------------------------
  **Figure 1. Individual Direct Messaging**

**Figure 2** shows a simplified architecture of the same environment
using Apache Pulsar as a data streaming platform using sink connectors.

![image](https://user-images.githubusercontent.com/80357022/113936746-3ac15680-97c6-11eb-95ca-02380f8198e5.png)

  ------------------------------------------
  **Figure 2. Data Streaming with Pulsar**
  ------------------------------------------

## Why Pulsar

One of the biggest advantages of Pulsar is its cost-effective
scalability. Pulsar two-layer architecture allows for independent scaling
of storage and processing power. Other Pulsar features include:

* Cloud Agnostic   
* Queues
* Lightweight
* Message transformations
* Friendly API
* Decoupled architecture
* Client libraries
* Data storage
* Connectors
* Cloud native features
* Containerization


## This POC

The POC consists of a python client that collects data from the national
weather service API, and writes the same data into Pulsar Topics. The
data from the Pulsar topics is then written into Elasticsearch for data
analytics and search, and into Astra for low-latency transactions.

**Figure 3** shows an overview of the data flow from left to right.

![image](https://user-images.githubusercontent.com/80357022/113937887-d2737480-97c7-11eb-91d2-8cd2c8bffb6d.png)

**Figure 3**. Data flow in POC

# Hands-On Implementation

## Create the Virtual Machines, Astra database and Containers

1.  Virtual machines can be created anywhere. For this POC, we use a
    free Azure account and the docker template available on the
    Microsoft marketplace
    [here](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/cloud-infrastructure-services.docker_ubuntu?tab=overview).
    Create two virtual machines. The first one will be used for
    Elasticsearch, and the second one, will be used for Pulsar. Optionally,
    you can host both applications on the same VM.

2.  Create an Astra database named "dbtest" from the Astra console and a
    keyspace with the same name.

2.1 Create a table with the following definition in the CQL console:

``` sql
CREATE TABLE dbtest.forecast (
key text PRIMARY KEY,
content text);
```

3.  Generate a token, and give it the appropriate role for read/write
    operations. We will use the "Admin User" role for this demo.

4.  Launch a Pulsar container using the following bash command:

``` bash
docker run -it \
-p 6650:6650 \
-p 8080:8080 \
-v \$PWD/data:/pulsar/data \
apachepulsar/pulsar:latest \
bin/pulsar standalone
```

Optionally, you can use the production-ready distribution of Apache
Pulsar, called "Luna Streaming", by following the instructions available
[here](https://docs.datastax.com/en/luna/streaming/1.0/quickstart-helm-installs.html).

5.  Launch an Elasticsearch container using the following bash command:

``` bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -v $PWD/data:/usr/share/elasticsearch/data --name elasticsearch elasticsearch:7.10.1
```
## Configuring Pulsar

Now that we have all the infrastructure components, it is time to configure
Pulsar and create topics and sink connectors.

Create a Pulsar-Astra sink to directly write into the Astra database messages stored
in Pulsar topics.

1.  To deploy the sink connector for Astra, download it from the DataStax
    [downloads](https://downloads.datastax.com/#apc) site and follow the
    steps listed in the
    [documentation](https://docs.datastax.com/en/pulsar-connector/1.4/pulsarInstall.html).

2.  Modify the sink configuration file. The Astra sink connector configuration requires several undocumented changes. Please refer to the sample file posted in the docs folder       of this POC for details and examples.

3.  Create a new sink by executing the following command.
    Note: replace the "example.yml" file by the name of your sink configuration file.
    
``` bash
bin/pulsar-admin sinks create --name forecast-sink --classname com.datastax.oss.sink.pulsar.StringCassandraSinkTask --sink-config-file conf/example.yml --sink-type cassandra-enhanced --tenant public --namespace default --inputs "persistent://public/default/forecast"
```

Create a Pulsar-Elasticsearch sink to directly write into the Astra database messages stored
in Pulsar topics.

1.  Deploy the Elasticsearch sink connector by following the steps described
    [here.](https://pulsar.apache.org/docs/en/io-elasticsearch-sink/)

2.  Create an Elasticsearch sink by executing the command below.
    Note: replace the "example.yml" file with the name of your sink configuration file

``` bash
bin/pulsar-admin sinks create --name elasticsearch-sink \
--sink-config-file conf/example.yaml \
--archive connectors/pulsar-io-elastic-search-2.7.0.nar  \
--tenant public --namespace default --inputs "persistent://public/default/forecast_elastic
```

The so created Astra sink connector created will read any messages entering the
"forecast" topic, and will write them directly into the "forecast" table
created of the "dbtest" keyspace in the Astra database. The Elasticsearch sink connector
will follow the same behavior for messages received in the
"*forecast_elastic*" topic.

## Streaming data

To start streaming data, download the Python client available in this repository, and execute the __main__.py file.

This application was written using Python 3.9, which can be downloaded from
[here](https://www.python.org/downloads/).
