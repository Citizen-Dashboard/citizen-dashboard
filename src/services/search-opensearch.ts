'use server'


import getOpenSearchClient from "./clients/opensearch-client.js";

interface SearchResult {
    _source: {
        agendaItemTitle: string;
        agendaItemSummary: string;
        agendaItemRecommendation: string;
        decisionRecommendations: string;
        decisionAdvice: string;
        itemStatus: string;
        reference: string;
    }
}

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
     * @method getSearchQuery
     * @description Get the search query for the OpenSearch index. We define the search query for the OpenSearch index in this method.
     * @param {string} term - The search term.
     * @returns {object} The search query.
     */
    static getSearchQuery(term:string) {
        return {
            "query":{
                "multi_match": {
                    "query": term,
                    "type": "best_fields", 
                    "fields": [
                        "agendaItemTitle^5",
                        "agendaItemSummary",
                        "agendaItemRecommendation^5",
                        "decisionRecommendations^10",
                        "decisionAdvice^10",
                        "decisionBodyName^10"
                    ],
                    "minimum_should_match": "2<60%"
                }
            },
            "sort": [
                {
                    "meetingDate": {
                    "order": "desc"
                    }
                }
            ], 
            "highlight": {
                "fields": {
                    "agendaItemTitle":{},
                    "agendaItemSummary":{},
                    "agendaItemRecommendation":{},
                    "decisionRecommendations":{},
                    "decisionAdvice":{}
                }
            }
        }
    }


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
            body: SearchClient.getSearchQuery(queryTerm)
        })
        console.log(response);
        console.info(`Found ${response?.hits.total.value} results`);
        return {
            results: this.sanitizeSearchResults(response?.hits.hits),
            total: response?.hits.total.value
        };
    }



    /**
     * @method sanitizeSearchResults
     * @description Sanitize the search results.
     * @param {array} searchResults - The search results.
     * @returns {array} The sanitized search results.
     */
    sanitizeSearchResults(searchResults: SearchResult[]) {
        return searchResults.map((result: SearchResult) => {
            return {
                title: result._source.agendaItemTitle,
                summary: result._source.agendaItemSummary,
                recommendation: result._source.agendaItemRecommendation,
                decisionRecommendations: result._source.decisionRecommendations,
                decisionAdvice: result._source.decisionAdvice,
                itemStatus: result._source.itemStatus,
                reference: result._source.reference
            }
        })
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
