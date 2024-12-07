'use server'

import { getSearchQuery, searchResultsLimit } from "@/services/clients/elastic-index-settings";
import { getHighlightedSearchResults, sanitizeSearchResults } from "@/services/SearchResultParser";
import { Client, ClientOptions, estypes } from "@elastic/elasticsearch";
import fs from "fs";
import { get } from "http";

class ElasticSearchClient {
    clientReady: boolean = false;
    indexName: string = process.env.elasticIndex || "DEFAULT_AGENDA_ITEMS_INDEX";
    client: Client | undefined;

    constructor(options: ClientOptions){
        this.client = new Client(options);
    }

    async init() {
        this.client?.ping()
            .then(() => {
                this.clientReady = true;
            })
            .catch((err) => {
                console.error(err);
                process.exit(1);
            });
    }

    
    async search(queryTerm: string) {

        if (!this.clientReady) {
            await this.init();
        }
        // const searchQuery = {
        //     index: this.indexName,
        //     /* query: {
        //         multi_match: {
        //             query: queryTerm,
        //             type: "best_fields", 
        //             fields: [
        //                 "ai_summary^10",
        //                 "agendaItemTitle^5",
        //                 "agendaItemSummary",
        //                 "agendaItemRecommendation^5",
        //                 "decisionRecommendations^10",
        //                 "decisionAdvice^10",
        //                 "decisionBodyName^10"
        //             ]
        //         }
        //     } */
        //    query: getSearchQuery(queryTerm).query,
        // }
        
        const searchQuery = {
            ...getSearchQuery(queryTerm),
            index: this.indexName,
        }
        const response = await this.client?.search<AgendaItemElasticDcoument>(searchQuery)
        if (!response) {
            return {
                results: []
            };
        }

        console.log(response.hits.total, typeof(response.hits.total))
        return {
            results: sanitizeSearchResults(response?.hits.hits as unknown as SearchResult[]),
            highlightedResults: getHighlightedSearchResults(response?.hits.hits as unknown as SearchResult[]),
            total: response?.hits.total ||0,
            limit: searchResultsLimit
        };
    }
}



async function createElasticSearchClient() {
    /* Note: This client requires the ca.crt file to be present in the same directory as the client. 
    *  Follow the instructions in the ElasticSearch-Server README.md to get the CA certificate.
    */
    const options: ClientOptions = {
        node: process.env.elasticLocalAPIEndpoint,
        auth: {
          username: process.env.elasticLocalUserName || "",
          password: process.env.elasticLocalPassword || ""
        },
        tls:{
          ca:fs.readFileSync(process.cwd() + "/src/services/ca.crt"),
          rejectUnauthorized:false
        }
    };

    const client = new ElasticSearchClient(options);
    await client.init()
    return client;
}

let elasticClient:ElasticSearchClient|undefined = undefined

export async function getSearchResults(queryTerm: string) {
    if(!elasticClient){
        elasticClient = await createElasticSearchClient() 
    }

    const results = await elasticClient.search(queryTerm)
    return results

}

