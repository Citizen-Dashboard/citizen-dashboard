# Introduction
This project contains three components:
1. An Indexer server
2. A Search server
3. A NextJS frontend

Both should be run in separate terminals/containers. 

**The Indexer server** is a continous running process that subscribe for messages published to the Kafka topic name defined in the environment variable `kafka_agendaItem_topic`. It  consumes agenda items from Kafka and indexes them in Elasticsearch. In Production, the Indexer server can be run in a cluster. 

> Note: The Indexer server will exit if the Kafka topic does not exist. Ensure that the DataAggregator service is run before starting the indexer server.


**The search server** provides a REST API and a NextJS frontend to search for agenda items in Elasticsearch. In Production, multiple instances of the search server can be run behind a load balancer for scalability.

**The NextJS frontend** is a simple web app that allows you to search for agenda items and view the results. It is built with NextJS and TypeScript. 

> NextJS supports running the frontend and backend servers in a single container, but for simplicity, we are using only the client side in this project (similar to a react project). However, we have included instructions and example for building server side component in the `ElasticSearch-Client\readme.md` file.


## Setup Instructions

### BEFORE SETUP: Update .env files
Create `.env` files in `elasticSearch-Client`, `elasticSearch-Server` and `ElasticSearch-Server\elasticsearch-container` folders.
Use the file named `local-env-file` for reference. The passwords can be anything, but make sure the Elastic password matches in all env files.


### 1. Start Kafka Container
Follow instructions in the DataAggregator project's README.md to start the kafka container. Copy the kafa container `REST_PORT` and `plainText_PORT` from the console, and update the '.env' file.

### 2. Run data aggregator
Follow instructions in the DataAggregator project's README.md to run the data aggregator. This ensures that agenda items are produced to the Kafka topic.

### 3. Start Elasticsearch Container
* Make sure you have docker and docker compose installed.
* Navigate to the elasticsearch-container directory
* Run the following command to start the container
```bash
docker compose up
```

> For the search server and indexer server to connect to the Elasticsearch container, you need to make sure that the elasticsearch CA certificate is installed on the server.

### 4. Copy CA certificate to the search server
1. Find the docker container name for the elasticsearch container using the command `docker ps`.

    You should see an output like this. Pick the name of any of the elastic search containers.

    ```bash
    a3f5b0b80ee6   docker.elastic.co/kibana/kibana:8.15.0                 "/bin/tini -- /usr/l…"   46 hours ago        Up About an hour (healthy)   0.0.0.0:5601->5601/tcp                                       elasticsearch-container-kibana-1
    c3581fd2bf7c   docker.elastic.co/elasticsearch/elasticsearch:8.15.0   "/bin/tini -- /usr/l…"   46 hours ago        Up About an hour (healthy)   9200/tcp, 9300/tcp                                           elasticsearch-container-es03-1
    ec9f80ce511d   docker.elastic.co/elasticsearch/elasticsearch:8.15.0   "/bin/tini -- /usr/l…"   46 hours ago        Up About an hour (healthy)   9200/tcp, 9300/tcp                                           elasticsearch-container-es02-1
    d436e2264d19   docker.elastic.co/elasticsearch/elasticsearch:8.15.0   "/bin/tini -- /usr/l…"   46 hours ago        Up About an hour (healthy)   127.0.0.1:9200->9200/tcp, 9300/tcp                           elasticsearch-container-es01-1
    ```

2. Copy the CA certificate to the Elasticsearch server
   Make sure you are in the `elasticsearch-server/server/elasticsearch` directory.
    ```bash
    docker cp elasticsearch-container-es01-1:/usr/share/elasticsearch/config/certs/ca/ca.crt ./ca.crt
    ```



### 4. Install npm package dependencies
* Run the following command to install the dependencies
```bash
npm install
```

### 5. Start the Indexer server
* Navigate to the `server` directory
* Run the following command to start the server
```bash
npm run indexer
```
Now the indexer server is running and is ready to consume agenda items from Kafka whenever they are produced by the DataAggregator server.
It will index the agenda items already produced in the Kafka topic to Elasticsearch.

### 6. Start the search server
* Navigate to the `server` directory
* Run the following command to start the server
```bash
npm run search
```
Now the search server is running and is ready to serve HTTP requests.


### 6. Make a search request'
Starting the **search server** with the `npm run search` command will also serve a nextJS frontend on port 3001. 
You should be able to access the nextJS web app by navigating to `http://127.0.0.1:3001` in your web browser.

If you just want to use the search server without the frontend, you can send a search request to the search server like this:
```bash
curl --location 'http://127.0.0.1:3001/search?query=sign%20employment%20district'
```
> The nextJS frontend is served from the `server/next_build` folder. Follow the instructions in the netJS frontend project to build static content and update the `server/next_build` folder.

### 7. Build and run the nextJS frontend
* Navigate to the `elasticsearch-client` directory
* Follow the instructions in the README.md file to build and run the nextJS frontend.