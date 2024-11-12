/**
 * Helper module that takes care of creating the right client depending on the environment.
 * Use `elasticClient` configuration from `.env` file to create a local or a cloud Client connector.
 * `process.env.elasticClient = 'local'` creates a local client connection
 * `process.env.elasticClient = 'cloud' creates a cloud client connection
 * 
 */
import {getLogger} from '../logging/logger.js';
const logger = getLogger(import.meta.url);

const clientType = process.env.elasticClient? process.env.elasticClient:'local';
logger.debug("use client", clientType, process.env.elasticClient)
let clientContainer;

switch (clientType) {
    case "elastic-cloud":
      clientContainer = await import("./cloud-client.js");
      break;
    case "aws-opensearch":
      clientContainer = await import("./opensearch-client.js")
      break;

    default:
      clientContainer = await import("./local-client.js");
        break;
}

const client = clientContainer.default
/* Esure we can reach the client. If client is not connected, exit the program with error code 1. */
client.ping()
  .then(response => console.log("You are connected to Elasticsearch!"))
  .catch(error => {
    console.error(error)
    logger.error(error)
    logger.error("Cannot connect to Elasticsearch. Exiting with error code 1.")
    process.exit(1)
  })


export default client;