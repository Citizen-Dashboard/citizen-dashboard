/**
 * @file local-client.js
 * @description A file for creating a local client for Elasticsearch. This is not to be used in production.
 * @version 1.0.0
 * @since 2024-07-23
 */


//used in server/elasticsearch/client.js
import { Client } from '@elastic/elasticsearch';
import {getLogger} from "../logging/logger.js";
/* for reading the ca.crt file */
import fs from 'fs';
import path from 'path';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const logger = getLogger(import.meta.url);
    
const __dirname = dirname(fileURLToPath(import.meta.url));

// create a local client using username and password authentication with TLS certificate
// security is not enabled in local deployment
const client = new Client({
    node: process.env.elasticLocalAPIEndpoint,
    auth: {
      username: process.env.elasticLocalUserName,
      password: process.env.elasticLocalPassword
    },
    tls:{
      ca:fs.readFileSync(path.resolve(__dirname, "ca.crt")),
      rejectUnauthorized:false
    }
});

/* Esure we can reach the client. If client is not connected, exit the program with error code 1. */
await client.ping()
  .then(response => console.log("You are connected to Elasticsearch!"))
  .catch(error => {
    logger.error(error)
    logger.error("Cannot connect to Elasticsearch. Exiting with error code 1.")
    process.exit(1)
  })


export default client; 