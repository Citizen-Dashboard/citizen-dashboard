'use server'

import { getSearchQuery, searchResultsLimit } from "@/services/clients/elastic-index-settings";
import getOpenSearchClient from "./clients/opensearch-client.js";
import { getHighlightedSearchResults, sanitizeSearchResults } from "@/services/SearchResultParser";



type OpenSearchClient = Awaited<Promise<PromiseLike<ReturnType<typeof getOpenSearchClient>>>>

/**
 * @class SearchClient
 * @description A class for searching an OpenSearch index.
 * Intializes the client with an index name and provides a search method.
 */
class SearchClient {
    client:OpenSearchClient|undefined;
    clientReady: boolean;
    indexName: string = process.env.elasticIndex || "DEFAULT_AGENDA_ITEMS_INDEX";
    

    /**
     * @constructor
     * @description Create an instance of an OpenSearchClient.
     * @param {string} indexName - The name of the OpenSearch index.
     */
     constructor(/* indexName:string */) {
        this.clientReady = false;
        // this.indexName = indexName;
    }


    /**
     * @method init
     * @description Initialize the OpenSearch client.
     * @returns {Promise<void>}
     */
    async init() {
        this.client = await getOpenSearchClient();
        this.client.ping()
            .then(() => {
                this.clientReady = true;
            })
            .catch((err: Error) => {
                console.error(err);
                process.exit(1);
            });
    }


    /**
     * @method search
     * @description Search the OpenSearch index.
     * @param {string} queryTerm - The search term.
     * @returns {Promise<object>} The search results.
     */
    async search(queryTerm:string) {
        console.info(`Searching for ${queryTerm}`);
        if (!this.clientReady) {
            await this.init();
        }
        const response = await this.client?.search({
            index: this.indexName,
            body: getSearchQuery(queryTerm)
        })
        console.log(response);
        console.info(`Found ${response?.hits.total.value} results`);
        return {
            results: sanitizeSearchResults(response?.hits.hits),
            highlightedResults: getHighlightedSearchResults(response?.hits.hits),
            total: response?.hits.total.value,
            limit: searchResultsLimit
        };
    }
}



async function createOpenSearchClient() {
    const client = new SearchClient();
    await client.init()
    return client;
}

let elasticClient:SearchClient|undefined = undefined

export async function getSearchResults(queryTerm: string) {
    if(!elasticClient){
        elasticClient = await createOpenSearchClient() 
    }

    const results = await elasticClient?.search(queryTerm)
    return results

}
