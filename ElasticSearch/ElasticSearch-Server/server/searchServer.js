/*
* @description
* This is the entry point for the search server. 
* This script initializes and runs the Search Server which provides a REST API to search for agenda items in Elasticsearch.
* It also hosts the static files of the nextJS app that provides the frontend.
* 
* @module searchServer
* 
* @example
* // To run the server:
* // node searchServer.js
*/

import 'dotenv/config'
import express from 'express';
import cors from 'cors';
import {initializeLogger, getLogger} from './logging/logger.js';
import ElasticSearchClient from './elasticsearch/search.js';

import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

initializeLogger("search-server");


const logger = getLogger(import.meta.url);

const app = express();
const port = 3001;


// logger middleware to log all requests
app.use((req,res,next) =>{
    req.time = new Date(Date.now()).toString();
    logger.info([req.method, req.hostname, req.path, req.time]);
    logger.debug({query: req.query, body: req.body, response: res});
    next();
});


// Enable cors for all routes so that the nexJS localhost dev on port 3000 can access the 
// server localhost on port 3001
// CORS will not be required in production

var corsOptions = {
    origin: 'http://localhost:3000',    // Enable cors for localhost client. Add other domains if needed.
    optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
  }
  
  app.options('*', cors(corsOptions));
  
  // Initialize the elastic search client. 
  // Make sure the elastic index is set in the .env file (or in the environment variables for production).
  const elasticSearchClient = new ElasticSearchClient(process.env.elasticIndex);



// Define the search route for the REST API that will be used by the nextJS app to search for agenda items.
app.get('/search', cors(corsOptions), async (req, res) => {
    logger.info('Searching for query: ' + req.query.query);
    const queryTerm = req.query.query;
    const searchResults = await elasticSearchClient.search(queryTerm);
    logger.debug('Search results: ' + searchResults);
    res.json(searchResults);
}); 


/* Define the static content folder for the nextJS app frontend.

Copy the Static files of the nextJS app into the next-build folder 
after running the build command. 
*/
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const nextJsStaticFolder = path.join(__dirname, 'next_build')

if(!fs.existsSync(nextJsStaticFolder)){
    logger.info("NextJS static folder not found. Not starting static file content. You can still use the /search rest API endpoint.");
}
else {
app.use(express.static(nextJsStaticFolder))
}



//start the Node server
app.listen(port, () => logger.info(`Server listening at http://localhost:${port}`));