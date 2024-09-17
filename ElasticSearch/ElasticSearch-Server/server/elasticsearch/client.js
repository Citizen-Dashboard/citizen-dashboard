/**
 * Helper module that takes care of creating the right client depending on the environment.
 * Use `elasticClient` configuration from `.env` file to create a local or a cloud Client connector.
 * `process.env.elasticClient = 'local'` creates a local client connection
 * `process.env.elasticClient = 'cloud' creates a cloud client connection
 * 
 */
const useLocalClient = (process.env.elasticClient === 'local');
console.log("use client", useLocalClient, process.env.elasticClient)
let clientContainer
if(useLocalClient){
    clientContainer = await import("./local-client.js");
}
else{
    clientContainer = await import("./cloud-client");
}

export default clientContainer.default