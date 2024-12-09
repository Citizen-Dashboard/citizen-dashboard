import client from "./client.js"
import { getLogger } from "../logging/logger.js";

const logger = getLogger(import.meta.url);

/**
 * @class ElasticSearchClient
 * @description A class for searching an Elasticsearch index.
 * Intializes the client with an index name and provides a search method.
 */
export default class ElasticSearchClient {
    /**
     * @method getSearchQuery
     * @description Get the search query for the Elasticsearch index. We define the search query for the Elasticsearch index in this method.
     * @param {string} term - The search term.
     * @returns {object} The search query.
     */
    static getSearchQuery(term) {
        return {
            "query":{
                "size":30,
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
     * @description Create an instance of an ElasticSearchClient.
     * @param {string} indexName - The name of the Elasticsearch index.
     */
    constructor(indexName) {
        this.client = client;
        this.clientReady = false;
        this.indexName = indexName;
    }


    /**
     * @method init
     * @description Initialize the Elasticsearch client.
     * @returns {Promise<void>}
     */
    async init() {
        this.client.ping()
            .then(() => {
                this.clientReady = true;
            })
            .catch((err) => {
                console.error(err);
                process.exit(1);
            });
    }


    /**
     * @method search
     * @description Search the Elasticsearch index.
     * @param {string} queryTerm - The search term.
     * @returns {Promise<object>} The search results.
     */
    async search(queryTerm) {
        logger.info(`Searching for ${queryTerm}`);
        if (!this.clientReady) {
            await this.init();
        }
        const response = await this.client.search({
            index: this.indexName,
            body: ElasticSearchClient.getSearchQuery(queryTerm)
        })
        console.log(response);
        logger.info(`Found ${response.hits.total.value} results`);
        return {
            results: this.sanitizeSearchResults(response.hits.hits),
            total: response.hits.total.value
        };
    }



    /**
     * @method sanitizeSearchResults
     * @description Sanitize the search results.
     * @param {array} searchResults - The search results.
     * @returns {array} The sanitized search results.
     */
    sanitizeSearchResults(searchResults) {
        return searchResults.map((result) => {
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