type agendaItem = {
    decisionBodyName?: string,
    itemStatus: strting
    title: string,
    summary: string,
    ai_summary:string,
    recommendation?: string,
    decisionRecommendations?: string,
    decisionAdvice?: string,
    reference: string,
    meetingDate: Date
}


type agendaItemHighlightInfo = {text:string, highlight:boolean}
type agendaItemHighlights = {
    decisionBodyName?: string,
    itemStatus: strting,
    ai_summary?: agendaItemHighlightInfo[],
    title:string,
    summary?:agendaItemHighlightInfo[],
    recommendation?:agendaItemHighlightInfo[],
    decisionRecommendations?:agendaItemHighlightInfo[] ,
    decisionAdvice?:agendaItemHighlightInfo[],
    reference: string,
    meetingDate: Date
}

/** todo: Update ElasticSearch document structure to match agendaItem type above */
type AgendaItemElasticDcoument = {
    decisionBodyName: string,
    itemStatus: strting
    agendaItemTitle: string,
    agendaItemSummary: string,
    ai_summary:string,
    agendaItemRecommendation?: string,
    decisionRecommendations?: string,
    decisionAdvice?: string,
    reference: string,
    meetingDate: Date
}

type searchResults = {
    results: agendaItem[]|never[],
    highlightedResults?: agendaItemHighlights[] | never[]
    total?: number
}

interface SearchResult {
    _source: AgendaItemElasticDcoument,
    highlight: {
        ai_summary?:string[],
        agendaItemTitle?:string[],
        agendaItemSummary?:string[],
        agendaItemRecommendation?:string[],
        decisionRecommendations?:string[],
        decisionAdvice?:string[],
        meetingDate: Date
    }
}
