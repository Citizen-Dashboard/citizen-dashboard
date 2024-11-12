/*
* @description
* The ElasticIndexer class is responsible for initializing the Elasticsearch index and adding documents to it.
* It uses the Elasticsearch client to connect to the Elasticsearch server and perform the necessary operations.
*/


import client from "./client.js";
import { getLogger } from '../logging/logger.js';

const logger = getLogger(import.meta.url);


export default class ElasticIndexer {
    constructor({indexName, indexMappings, indexSettings}) {
        this.client = client;
        this.indexName = indexName;
        this.indexMappings = indexMappings;
        this.indexSettings = indexSettings;
    }

    async init() {
        //step 1: check if client is running
        await this.client.ping();
        //will throw error if ping failed

        //if index doesn't exist, create it and load documents
        if (await this.client.indices.exists({ index: this.indexName })) {
            //exit. index already exists
            logger.debug('Index already exists. Proceeding to data load');
        } else {
            logger.debug("Index does not exist. Creating new index, mapping and loading data");
            await this.setupIndex();
            await this.client.indices.open({ index: this.indexName });
        }
        logger.info("Indexer initialized")
    }

    async setupIndex() {
        logger.info(`Creating index ${this.indexName}`);
        await this.client.indices.create({ 
            index: this.indexName,
            body: {
                settings: this.indexSettings,
                mappings: this.indexMappings,
            }
        });
        
        logger.info(`Index ${this.indexName} created`);
    }


    async addDocument(document) {
        try {
            const response = await this.client.index({
                index: this.indexName,
                body: document,
                id: document.agendaItemId
            });
            logger.debug(`Document indexed successfully: ${response.result}`);
            return response;
        } catch (error) {
            logger.error("Error indexing document");
            throw error;
        }
    }
}

/* Sample Data
{
            "id": "ID_136274",
            "termId": 8,
            "agendaItemId": 136274,
            "councilAgendaItemId": 136274,
            "decisionBodyId": 2744,
            "meetingId": 24669,
            "itemProcessId": 6,
            "decisionBodyName": "Confronting Anti-Black Racism Advisory Committee",
            "meetingDate": 1725422400000,
            "reference": "2024.CR4.3",
            "termYear": "2024",
            "agendaCd": "CR",
            "meetingNumber": "4",
            "itemStatus": "RECEIVED",
            "agendaItemTitle": "Data for Equity",
            "agendaItemSummary": "<p>The purpose of the presentation is to provide an overview of the City&rsquo;s Data for Equity Strategy and share key components and information on the work, including a focus on Black Data Governance.</p>",
            "agendaItemRecommendation": "",
            "decisionRecommendations": "<p>The&nbsp;Confronting Anti-Black Racism Advisory Committee received the item for information.&nbsp;</p>",
            "decisionAdvice": "<p>Debbie Burke-Benn, Director, Equity and Human Rights, People and Equity; Srijoni Rahman, Manager, Equity and Data for Equity Unit, People and Equity; Jemal Demeke, Researcher, Wellesley Institute; and Fiqir Worku, Researcher, Black Health Alliance, gave a presentation on&nbsp;Data for Equity.</p>",
            "subjectTerms": "boards of management, committee meetings, equity; boards of directors; boards of governors, employment equity; fair wage; pay equity",
            "wardId": ["1"]
        }
            */