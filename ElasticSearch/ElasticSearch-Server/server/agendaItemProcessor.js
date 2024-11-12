/**
 * @fileoverview This module defines the AgendaItemProcessor class for processing agenda items from Kafka and indexing them in Elasticsearch.
 * 
 * @module AgendaItemProcessor
 * 
 * @description
 * The AgendaItemProcessor class sets up a Kafka consumer to listen for new agenda items,
 * and an Elasticsearch indexer to store these items. When a new agenda item is received,
 * it is processed and added to the Elasticsearch index. The kafka consumer is configured to
 * use the kafka_agendaItem_topic and the kafka_agendaItem_group environment variables so we 
 * can run this application in a cluster.
 * 
 * @example
 * const processor = new AgendaItemProcessor();
 * processor.init();
 */

import KafkaConsumer from "./kafka/kafka_consumer.js";
import ElasticIndexer from "./elasticsearch/indexer.js";
import { indexMappings, indexSettings} from "./elasticsearch/elastic-index-settings.js"
import {getLogger} from "./logging/logger.js";


const logger = getLogger(import.meta.url);


export default class AgendaItemProcessor {
    constructor(){
        /* 
        * @description
        * The constructor initializes a KafkaConsumer for listening to agenda items and an ElasticIndexer for storing them.
        * It uses environment variables for configuration.
        */
        this.kafkaConsumer = new KafkaConsumer(process.env.kafka_agendaItem_topic);
        this.elasticIndexer = new ElasticIndexer({indexName:process.env.elasticIndex, indexMappings, indexSettings});
    }

    async init(){
        /* 
        * @description
        * Initializes the Elasticsearch indexer and starts consuming messages from Kafka.
        * This method should be called by the application that initilizes the AgendaItemProcessor before using it to process agenda items.
        */
        await this.elasticIndexer.init();
        this.kafkaConsumer.consume(this.processAgendaItem.bind(this));
    }

    async processAgendaItem(key, agendaItem){
        /* 
        * @description
        * Processes an agenda item by adding it to the Elasticsearch index.
        * This method is called by the KafkaConsumer when a new agenda item is received.
        */
        logger.debug("Processing agenda item %o", agendaItem);  
        try{
            logger.info("Adding agenda item to elasticsearch", {itemId: agendaItem.id});
            const elasticResponse = await this.elasticIndexer.addDocument(agendaItem);
            logger.debug("Elastic response", elasticResponse);
        }
        catch(error){
            logger.error("Error processing agenda item", error);
        }
    }
}