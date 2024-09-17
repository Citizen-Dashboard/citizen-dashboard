/**
 * @description
 * This script creates a Kafka consumer to consume messages from a Kafka topic.
 * It uses the KafkaJS library to connect to the Kafka server and consume messages from a specified topic.
 */

import { Kafka, logLevel } from 'kafkajs';
import KafkaAdmin from './kafka_admin.js';
import {getLogger} from '../logging/logger.js';

const logger = getLogger(import.meta.url);

/**
 * @class KafkaConsumer
 * @description A class for consuming messages from a Kafka topic.
 * Initializes the Kafka client and provides methods to consume messages from a specified topic.
 */
export default class KafkaConsumer {
  static errorTypes = ['unhandledRejection', 'uncaughtException']
  static signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

  /**
   * @constructor
   * @description Create an instance of a KafkaConsumer. Note that this creates a new connection to the Kafka server,
   * different from the kafka_admin so that the connections can be distingushed in the audit logs.
   * 
   * @param {string} topic - The name of the Kafka topic to consume messages from.
   * 
   */
  constructor(topic) {
    logger.info(`Configuring consumer on port: ${process.env.Plaintext_Ports}`);
    this.kafka = new Kafka({
      clientId: 'agenda-item-consumer',
      brokers: [`localhost:${process.env.Plaintext_Ports}`],
      logLevel: logLevel.INFO
    });

    this.consumer = this.kafka.consumer({ 
      // Consumers always require a groupId so Kafka can keep track of messages sent to consumer clusters connected to the same group.
      //additional configurations might be needed in the future, but this is the basic setup for now.
      groupId: process.env.kafka_agendaItem_group
    });
    
    this.topic = topic;
    this.topicReady = false;  //this will be set to true later when we start to consume messages from the topic.
    this.registerErrorHandlers();
    logger.info(`KafkaConsumer initialized for topic: ${this.topic}`);
  }


  /**
   * @method consume
   * @description Consume messages from the Kafka topic.
   * @param {function} callback - The callback function to handle the consumed messages.
   * @returns {Promise<boolean>} - Returns true if the topic is ready and subscription has been setup to consume messages, false otherwise.
   */

  async consume(callback) {
    if (!this.topicReady) {
        this.topicReady = await KafkaAdmin.topicExists(this.topic);
        logger.info(`Topic ${this.topic} available status: ${this.topicReady}`);
        if (!this.topicReady){
            logger.error(`ERROR: Topic ${this.topic} is not ready`);
            return false;
        }
    }
    
    await this.consumer.connect();
    await this.consumer.subscribe({ topic: this.topic, fromBeginning: true });
    logger.info(`Subscribed to topic: ${this.topic}`);
    
    try {
      await this.consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
          const key = message.key ? message.key.toString() : 'None';
          const value = JSON.parse(message.value.toString());
          callback(key, value);
          logger.debug(`Consumed event from topic ${topic}: key = ${key} value = ${value}`);
        },
      });
      return true;
    } catch (error) {
      logger.error(`Error while consuming message: ${error}`);
      return false;
    }
  }


  /**
   * @method registerErrorHandlers
   * @description Register error handlers for the Kafka consumer.
   * When an error occurs, the consumer will disconnect and the process will exit with a status code of 1.
   * @returns {void}
   */
  registerErrorHandlers(){
    KafkaConsumer.errorTypes.forEach(type => {
      process.on(type, async e => {
        try {
          logger.error(`process.on ${type}`, e)
          await this.consumer.disconnect()
          logger.info(`consumer disconnected. Exiting...`)
          process.exit(1)
        } catch (_) {
          logger.info(`failed trying to disconnect from Kafka. Exiting...`)
          process.exit(1)
        }
      })
    })


    /**
     * @method registerSignalTraps
     * @description Register signal traps for the Kafka consumer.
     * When a signal is received, the consumer will disconnect and the process will exit with a status code of 0.
     * @returns {void}
     */
    KafkaConsumer.signalTraps.forEach(type => {
      process.once(type, async () => {
        try {
          logger.info(`process.once signalTrap ${type}`)
          await this.consumer.disconnect()
          logger.info(`consumer disconnected. Exiting...`)
        } finally {
          process.kill(process.pid, type)
        }
      })
    })
  }

  /**
   * @method close
   * @description Close the Kafka consumer.
   * @returns {Promise<void>}
   */
  async close() {
    await this.consumer.disconnect();
  }
}