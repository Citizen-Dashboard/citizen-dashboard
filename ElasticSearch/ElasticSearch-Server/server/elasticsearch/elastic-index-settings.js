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
        'ai_summary': { type: 'text', analyzer: 'all_terms_analyzer', search_analyzer: 'my_stop_analyzer', search_quote_analyzer: 'all_terms_analyzer' },
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