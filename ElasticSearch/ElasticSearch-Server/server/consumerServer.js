
/**
 * @fileoverview This is the entry point for the consumer server that consumes 
 * agenda items from Kafka and indexes them in Elasticsearch. 
 * 
 * @module consumerServer
 * 
 * 
 * @description
 * This server script sets up a Kafka consumer to process agenda items and potentially index them
 * in Elasticsearch. The kafka consumer is configured to use the kafka_agendaItem_topic and the 
 * kafka_agendaItem_group environment variables so we can run this application in a cluster.
 * 
 * @example
 * // To run the server:
 * // node consumerServer.js
 */

import 'dotenv/config'
import {initializeLogger, getLogger} from './logging/logger.js';
initializeLogger("consumer-server");

import AgendaItemProcessor from './agendaItemProcessor.js';


const logger = getLogger(import.meta.url);


const agendaItemProcessor = new AgendaItemProcessor();
agendaItemProcessor.init();
logger.info("Consumer server initialized");