type agendaItem = {
    decisionBodyName: string,
    itemStatus: strting
    title: string,
    summary: string,
    recommendation: string | undefined,
    decisionRecommendations: string | undefined,
    decisionAdvice: string | undefined,
    reference: string
}


/** todo: Update ElasticSearch document structure to match agendaItem type above */
type AgendaItemElasticDcoument = {
    decisionBodyName: string,
    itemStatus: strting
    agendaItemTitle: string,
    agendaItemSummary: string,
    agendaItemRecommendation?: string,
    decisionRecommendations?: string,
    decisionAdvice?: string,
    reference: string
}

type searchResults = {
    results: agendaItem[]|never[],
    total?: number
}
