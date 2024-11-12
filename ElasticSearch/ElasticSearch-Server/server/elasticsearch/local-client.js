/**
 * @file local-client.js
 * @description A file for creating a local client for Elasticsearch. This is not to be used in production. Refer to client.js to see how to change the client.
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

export default client; 