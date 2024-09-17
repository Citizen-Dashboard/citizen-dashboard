//in server/elasticsearch/client.js
import { Client } from '@elastic/elasticsearch';

const client = new Client({
    node: process.env.elasticCloudAPIEndpoint,
  cloud: {
    id: process.env.elasticCloudID,
  },
  auth: {
    // username: process.env.elasticCloudUserName,
    // password: process.env.elasticCloudPassword
    apiKey: process.env.elasticSearchApiKey //get this from the elastic cloud dashboard
  },
});

client.ping()
  .then(response => console.log("You are connected to Elasticsearch!"))
  .catch(error => console.error("Elasticsearch is not connected."))

  export default client; 