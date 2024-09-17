/*
* @description
* Yyou can use this script to create an API key to connect to the Elasticsearch cluster.
* This is the recommended way to connect to the Elasticsearch cluster from the client, without using the username and password.
*
* This script creates an API key for the Elasticsearch cluster.
*
*/


require('dotenv').config()
const elasticClient = require("./client");

/*
* @description
* This function creates an API key for the Elasticsearch cluster.
* It uses the Elasticsearch client to connect to the Elasticsearch server and perform the necessary operations.
*/
async function generateAPIKeys(params) {

    const body = await elasticClient.security.createApiKey({
        name:"es-demo-api-key",
        role_descriptors:{
            es_writer: {
                cluster: ["all"],
                index: [
                    {
                        names: ['es-demo'],
                        privileges:['create_index', 'write', 'read', 'manage']
                    }
                ]
            }
        }
    })
    return Buffer.from(`${body.id}:${body.api_key}`).toString('base64');
}


generateAPIKeys()
  .then(console.log)
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
  