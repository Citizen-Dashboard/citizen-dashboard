export function sanitizeSearchResults(searchResults: SearchResult[]):agendaItem[] {
    return searchResults.map((result: SearchResult) => {
        return {                  
                title: result._source.agendaItemTitle,
                summary: result._source.agendaItemSummary,
                ai_summary: result._source.ai_summary,
                recommendation: result._source.agendaItemRecommendation,
                decisionRecommendations: result._source.decisionRecommendations,
                decisionAdvice: result._source.decisionAdvice,
                itemStatus: result._source.itemStatus,
                reference: result._source.reference,
                meetingDate: result._source.meetingDate
        }
    })
}


export function getHighlightedSearchResults(searchResults: SearchResult[]): agendaItemHighlights[]{
    return searchResults.map((result: SearchResult) => {
        return { 
            ai_summary:highlightPhrases(result._source.ai_summary,result.highlight?.ai_summary),
            title:result._source.agendaItemTitle,
            summary:highlightPhrases(result._source.agendaItemSummary,result.highlight?.agendaItemSummary),
            recommendation:highlightPhrases(result._source.agendaItemRecommendation,result.highlight?.agendaItemRecommendation),
            decisionRecommendations:highlightPhrases(result._source.decisionRecommendations,result.highlight?.decisionRecommendations),
            decisionAdvice:highlightPhrases(result._source.decisionAdvice,result.highlight?.decisionAdvice),
            reference: result._source.reference,
            itemStatus: result._source.itemStatus,
            meetingDate: result._source.meetingDate
        }
    })
}


function highlightPhrases(text?:string, highlights?:string[]) {
    /* Find all the emphaisised words to highlight */
    if(text===undefined)
        return undefined

    const regex = /<em>(.*?)<\/em>/g;
    let phrasesToHighlight:{[key:string]:string} = {}
    phrasesToHighlight = highlights?.reduce((agg, item)=>{
            const localMatches = item.match(regex);
            localMatches && localMatches.forEach(match => {
                match = match.replace(/<\/?em>/g, '');
                agg[match] = match;
            })
            return agg;
        }, phrasesToHighlight) || {}

    const markedText = Object.keys(phrasesToHighlight).reduce((textToHighlight, phrase)=>{
        return textToHighlight.replaceAll(phrase, `<<<bold>>>${phrase}<<</bold>>>`)
    }, text)

    const markedTextRegex= /(<<<bold>>>.*?<<<\/bold>>>)/g;
    const textParts:agendaItemHighlightInfo[] = markedText.split(markedTextRegex).map(textPart=>{
        const highlight = /<<<bold>>>/.test(textPart);
        return {
            text: textPart.replace(/<<<\/?bold>>>/g,"").replace(/$\\s*/,"&nbsp;").replace(/^\\s*/, "&nbsp;"),
            highlight:highlight
        }
    })
    
    return textParts;
}