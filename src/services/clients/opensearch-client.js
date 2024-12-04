'use server'


/**
 * @module opensearch-client
 * @description This module provides an OpenSearch client singleton that connects to an OpenSearch cluster using AWS SigV4 signing for authentication. 
 * It includes methods for checking the existence of indices, creating new indices, and opening existing indices. 
 * The client is designed to bridge the OpenSearch API methods with the Elasticsearch JavaScript API methods.
 * 
 * @requires @opensearch-project/opensearch
 * @requires @opensearch-project/opensearch/aws
 * @requires @aws-sdk/credential-providers
 * 
 * @example
 * import client from "./opensearch-client.js";
 * client.indices.exists({ index: 'my-index' })
 *   .then(exists => console.log(`Index exists: ${exists}`))
 *   .catch(err => console.error(err));
 */


import {Client} from "@opensearch-project/opensearch"
import {AwsSigv4Signer} from '@opensearch-project/opensearch/aws'
import { fromTemporaryCredentials } from "@aws-sdk/credential-providers";


/**
 * @class OpenSearchClient
 * @description This class is responsible for creating an OpenSearch client that connects to an OpenSearch cluster using AWS SigV4 signing for authentication.
 * It handles the creation of the client and provides methods for interacting with OpenSearch indices. It also provides wrapper methods to bridge Opensearch 
 * API methods and ElasticSEarch Javascript API methods.
 */

  /**
   * @constructor
   * @param {string} AWS_REGION - The AWS region where the OpenSearch service is hosted.
   * @throws {Error} Will throw an error if the AWS region is not specified in the environment variables.
   */

 
/**
 * @method indices.exists
 * @description Checks if a specified index exists in the OpenSearch cluster.
 * @param {string} indexName - The name of the index to check.
 * @returns {Promise<boolean>} A promise that resolves to true if the index exists, false otherwise.
 */

/**
 * @method indices.create
 * @description Creates a new index in the OpenSearch cluster.
 * @param {string} indexName - The name of the index to create.
 * @param {object} settings - The settings for the new index.
 * @returns {Promise<object>} A promise that resolves to the response from the OpenSearch cluster.
 */

/**
 * @method indices.open
 * @description Opens a previously closed index in the OpenSearch cluster.
 * @param {string} indexName - The name of the index to open.
 * @returns {Promise<object>} A promise that resolves to the response from the OpenSearch cluster.
 */

class OpenSearchClient {
   
  constructor(){
    const AWS_REGION = process.env.AWS_REGION;

    console.debug("creating client for :", {"region":AWS_REGION});
    const timestamp = (new Date()).getTime();
    this.client = new Client({
      ...AwsSigv4Signer({
        region: AWS_REGION,
        service: 'es',
        // Must return a Promise that resolve to an AWS.Credentials object.
        // This function is used to acquire the credentials when the client start and
        // when the credentials are expired.
        // The Client will refresh the Credentials only when they are expired.
        // With AWS SDK V3, Credentials.refreshPromise is used when available to refresh the credentials.
      
        // Example with AWS SDK V3:
        getCredentials: fromTemporaryCredentials({
          // Required. Options passed to STS AssumeRole operation.
          params: {
            // Required. ARN of role to assume.
            RoleArn: process.env.opensearchAccessRole,
            // Optional. An identifier for the assumed role session. If skipped, it generates a random
            // session name with prefix of 'aws-sdk-js-'.
            RoleSessionName: `ctto-node-server-${timestamp}`,
            // Optional. The duration, in seconds, of the role session. 3600=1 hour
            DurationSeconds: 3600,
            // ... For more options see https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
          },
          // Optional. Custom STS client configurations overriding the default ones.
          clientConfig: { region:process.env.AWS_REGION }
        }),
      }),
      node: process.env.opensearchCloudServiceURI, // OpenSearch domain URL
    });

    /* Create a wrapper to replicate elasticSearch JS API's client.indices object */
    this.indices = {
      exists: this.index_exists_wrapper.bind(this),
      create: this.create_index_wrapper.bind(this),
      open: this.open_index_wrapper.bind(this)
    }
  }

  /**
   * @method getClient
   * @description Retrieves the OpenSearch client instance.
   * @returns {Client} The OpenSearch client instance used for making requests to the OpenSearch cluster.
   */
  getClient(){
    return this.client
  }


  /**
 * @method index_exists_wrapper
 * @description Checks if a specified index exists in the OpenSearch cluster. Implements wrapper around Opensearch javascript
 * method to provide an elasticSearch Javascript api style interface. 
 * @param {string} indexName - The name of the index to check.
 * @returns {Promise<boolean>} A promise that resolves to true if the index exists, false otherwise.
 */
  async index_exists_wrapper(params){
    return new Promise((resolve, reject)=>{
      try {
        this.client.indices.exists(params, (err, resp)=>{
          if(err) reject(err);
          resolve(resp.body);
        })
      } catch (err) {
        reject(err)
      }
    })
  }

  /**
   * @method ping
   * @description Checks the connection to the OpenSearch cluster. 
   * This method sends a ping request to the OpenSearch server to verify if it is reachable and responsive.
   * @returns {Promise<boolean>} A promise that resolves to true if the server is reachable, false otherwise.
   */
  async ping(){
    return await this.client.ping()
  }

  /**
 * @method create_index_wrapper
 * @description Creates a new index in the OpenSearch cluster. Implements wrapper around Opensearch javascript
 * method to provide an elasticSearch Javascript api style interface. 
 * @param {string} indexName - The name of the index to create.
 * @param {object} settings - The settings for the new index.
 * @returns {Promise<object>} A promise that resolves to the response from the OpenSearch cluster.
 */
  async create_index_wrapper(params){
    return await this.client.indices.create(params)
  }
  
/**
 * @method open_index_wrapper
 * @description Opens an index in the OpenSearch cluster.Implements wrapper around Opensearch javascript
 * method to provide an elasticSearch Javascript api style interface. 
 * @param {string} indexName - The name of the index to open.
 * @returns {Promise<object>} A promise that resolves to the response from the OpenSearch cluster.
 */
  async open_index_wrapper(params){
    return await this.client.indices.open(params)
  }

/**
 * @method index
 * @description Indexes a document.Implements wrapper around Opensearch javascript
 * method to provide an elasticSearch Javascript api style interface. 
 * @param {string} indexName - The name of the index to open.
 * @returns {Promise<object>} A promise that resolves to the response from the OpenSearch cluster.
 */
  async index(params){
    return await this.client.index(params);
  }

  async search(params){
    const apiResponse = await this.client.search(params);
    if(apiResponse.statusCode==200){
      return apiResponse.body
    }
    else {
      console.error(`Opensearch Request failed with status ${apiResponse.body.statusCode}` )
      return {hits:{hits:[], total:{value:0, relation:eq}}}
    }
  }
}

//Create the singleton openSearchClientInstance
const openSearchClientInstance = new OpenSearchClient()

export default async function getOpenSearchClient() {
  return openSearchClientInstance;
}