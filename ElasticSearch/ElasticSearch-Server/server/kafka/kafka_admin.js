/*
* @description
* This script creates a Kafka admin client to manage Kafka topics.
* It uses the KafkaJS library to connect to the Kafka server and provides methods to check if a topic exists and to create a topic if it does not exist.
*/

import { Kafka } from 'kafkajs';
import {getLogger} from '../logging/logger.js';

const logger = getLogger(import.meta.url);

/**
 * @class KafkaAdmin
 * @description A class for managing Kafka topics.
 * Initializes the Kafka client and provides methods to check if a topic exists and to create a topic if it does not exist.
 */
class KafkaAdmin {
    /**
     * @constructor
     * @description Create an instance of a KafkaAdmin.
     * Initializes the Kafka client. Uses environment variables to connect to the right Kafka server and port.
     */
    constructor() {
        this.kafka = new Kafka({
            clientId: 'kafka-admin',
            brokers: [`${process.env.Kafka_Host}:${process.env.Plaintext_Ports}`],
        });

        this.admin = this.kafka.admin();
    }

    /**
     * @method connect
     * @description Connect to the Kafka server.
     * @returns {Promise<void>}
     */
    async connect() {
        await this.admin.connect();
    }

    /**
     * @method disconnect
     * @description Disconnect from the Kafka server.
     * @returns {Promise<void>}
     */
    async disconnect() {
        await this.admin.disconnect();
    }

    /**
     * @method topicExists
     * @description Check if a topic exists.
     * @param {string} topicName - The name of the topic to check.
     * @returns {Promise<boolean>} - Returns true if the topic exists, false otherwise.
     */
    async topicExists(topicName) {
        try {
            await this.connect();
            const topics = await this.admin.listTopics();
            return topics.includes(topicName);
        } catch (error) {
            logger.error(`Error occurred while checking if topic exists: ${error}}`);
            return false;
        } finally {
            await this.disconnect();
        }
    }

    /**
     * @method createTopic
     * @description Create a topic.
     * @param {string} topicName - The name of the topic to create.
     * @param {number} numPartitions - The number of partitions for the topic.
     * @param {number} replicationFactor - The replication factor for the topic.
     * @returns {Promise<boolean>} - Returns true if the topic was created successfully, false otherwise.
     */
    async createTopic(topicName, numPartitions = 1, replicationFactor = 1) {
        try {
            await this.connect();
            await this.admin.createTopics({
                topics: [{
                    topic: topicName,
                    numPartitions,
                    replicationFactor
                }]
            });
            logger.info(`Topic ${topicName} created successfully`);
            return true;
        } catch (error) {
            logger.error(`Error occurred while creating topic: ${error}`);
            return false;
        } finally {
            await this.disconnect();
        }
    }
}

export default new KafkaAdmin();