export const indexMappings = {
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


export const indexSettings = {
    index: {
      number_of_shards: process.env.elasticShardsCount,
      number_of_replicas: process.env.elasticReplicasCount,
    },
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

export const searchResultsLimit = 30; 


 /**
 * @method getSearchQuery
 * @description Get the search query for the OpenSearch index. We define the search query for the OpenSearch index in this method.
 * @param {string} term - The search term.
 * @returns {object} The search query.
 */
 export function getSearchQuery(term:string) {
    return {
        "size":`${searchResultsLimit}`,
        "query":{
            "multi_match": {
                "query": term,
                "type": "best_fields", 
                "fields": [
                    "ai_summary^10",
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
                "ai_summary":{},
                "agendaItemSummary":{},
                "agendaItemRecommendation":{},
                "decisionRecommendations":{},
                "decisionAdvice":{}
            }
        }
    }
}