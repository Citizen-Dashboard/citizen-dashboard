/*
* @description
* The ElasticIndexer class is responsible for initializing the Elasticsearch index and adding documents to it.
* It uses the Elasticsearch client to connect to the Elasticsearch server and perform the necessary operations.
*/


import client from "./client.js"

export default class ElasticIndexer {
    constructor(indexName) {
        this.client = client;
        this.indexName = indexName;
    }

    async init() {
        //step 1: check if client is running
        await this.client.ping();
        //will throw error if ping failed

        //if index doesn't exist, create it and load documents
        if (await this.client.indices.exists({ index: this.indexName })) {
            //exit. index already exists
            console.log('Index already exists. Skipping data load');
        } else {
            console.log("Index does not exist. Creating new index, mapping and loading data");
            await this.client.indices.create({ index: this.indexName }, (err, res, status) => {
                console.log(err, res, status);
            });
            await this.client.indices.close({ index: this.indexName });
            await this.setupIndex();
            await this.client.indices.open({ index: this.indexName });
        }
    }

    async setupIndex() {
        console.log("Defining analyzer for index");
        await this.client.indices.putSettings({
            index: this.indexName,
            body: {
                analysis: {
                    analyzer: {
                        "all_terms_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase"
                            ]
                        },
                        "my_stop_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop"
                            ]
                        }
                    },
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        }
                    }
                }
            }
        });

        console.log("Creating Mapping index");
        await this.client.indices.putMapping({
            index: this.indexName,
            body: {
                properties: {
                    'id': { enabled: false },
                    'agendaItemId': { enabled: false },
                    'decisionBodyId': { enabled: false },
                    'decisionBodyName': { type: 'keyword' },
                    'reference': { type: 'keyword' },
                    'meetingDate': { type: 'date', format: 'epoch_millis' },
                    'meetingId': { enabled: false },
                    'termYear': { enabled: false },
                    'agendaCd': { enabled: false },
                    'itemStatus': { type: 'keyword' },
                    'agendaItemTitle': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
                    'agendaItemSummary': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
                    'agendaItemRecommendation': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
                    'decisionRecommendations': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
                    'decisionAdvice': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
                    'subjectTerms': { type: 'keyword' },
                    'wardId': { type: 'keyword' }
                }
            }
        }, (err, resp, status) => {
            if (err) {
                console.error(err, status);
            } else {
                console.log('Successfully Created Index mapping', status, resp);
            }
        });
    }


    async addDocument(document) {
        try {
            const response = await this.client.index({
                index: this.indexName,
                body: document,
                id: document.agendaItemId
            });
            console.log(`Document indexed successfully: ${response.result}`);
            return response;
        } catch (error) {
            console.error(`Error indexing document: ${error}`);
            throw error;
        }
    }
}

/*
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