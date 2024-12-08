//this will be rendered server side.

/** 
 * Use @/services/search-elastic to connect to Elasticsearch
 * Use @/services/search-opensearch to connect to AWS OpenSearch
 */
// import  {getSearchResults} from '@/services/search-elastic'
import  {getSearchResults} from '@/services/search-opensearch'
import Image from "next/image";
import Link from "next/link";
import aiContentImage from '@/images/aiContent.svg';
import Chip, {OutlinedChip} from '@/app/Chip'
/**
 * Server-side Search Results component that displays agenda items based on a search query.
 * 
 * This component:
 * - Fetches search results server-side using the provided query
 * - Renders a list of agenda items with their details
 * - Displays title, status, decision body, advice, recommendations and summary for each item
 * - Provides links to the full agenda items on toronto.ca
 * - Handles errors gracefully by logging them and returning empty results
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} props.query - The search query string to filter agenda items
 * @returns {Promise<JSX.Element>} A promise that resolves to the rendered search results
 */



const AiGeneratedContent = ({children}:{children:React.ReactNode})=>{
    return (
        <><OutlinedChip className='inline-block mr-3'><Image className="inline m-0 mr-1" src={aiContentImage} alt="AI generated summary"/>AI</OutlinedChip>{children}</>
    )
}

// const AiGeneratedContent = ({children}:{children:React.ReactNode})=>{
//     return (
//         <div className="chat chat-start">
//             <div className="chat-image avatar">
//                     <Image className="inline m-0 mr-1" src={aiContentImage} alt="AI generated summary"/>AI
//             </div>
//             <div className="chat-bubble bg-gray-200 text-gray-700">{children}</div>
//         </div>
//     )
// }


function formatDate(timestamp:Date) { 
    const date = new Date(timestamp); 
    const options:Intl.DateTimeFormatOptions = { month: 'short', day: '2-digit', year: 'numeric' }; 
    return date.toLocaleDateString('en-US', options); 
}

const highlightInfoToJSX = (highlightInfo:agendaItemHighlightInfo[])=>{
    const highlightJSX = highlightInfo.map((textInfo, index)=>{
        if(textInfo.highlight){
            return <b key={index}>{textInfo.text}</b>
        }
        else {
            return <>{textInfo.text}</>
        }
    })
    return <>{...highlightJSX}</>
}
const getHIghlightedResultsJSXMap = (highlightedResults:agendaItemHighlights[]) =>{
    return highlightedResults.map((agendaItem)=>{
        return {
            decisionBodyName: agendaItem.decisionBodyName?(<p>{agendaItem.decisionBodyName}</p>):<></>,
            itemStatus: agendaItem.itemStatus,
            title: agendaItem.title,
            summary:agendaItem.summary?<><h3>Summary:</h3><p>{highlightInfoToJSX(agendaItem.summary)}</p></>:<></>,
            ai_summary:agendaItem.ai_summary?<><AiGeneratedContent>{highlightInfoToJSX(agendaItem.ai_summary)}</AiGeneratedContent></>:<></>,
            recommendation: agendaItem.recommendation?<><h3>Recommendation:</h3><p>{highlightInfoToJSX(agendaItem.recommendation)}</p></>:<></>,
            decisionRecommendations: agendaItem.decisionRecommendations?<><h3>Decision Recommendation:</h3><p>{highlightInfoToJSX(agendaItem.decisionRecommendations)}</p></>:<></>,
            decisionAdvice: agendaItem.decisionAdvice?<><h3>Decision Advice:</h3><p>{highlightInfoToJSX(agendaItem.decisionAdvice)}</p></>:<></>,
            reference: agendaItem.reference,
            meetingDate: formatDate(agendaItem.meetingDate)
        }
    })
}


const getTextResultsJSXMap =(sourceResults:agendaItem[]) =>{
    return sourceResults.map((agendaItem)=>{
        return {
            decisionBodyName: agendaItem.decisionBodyName?(<p>{agendaItem.decisionBodyName}</p>):<></>,
            itemStatus: agendaItem.itemStatus,
            title: agendaItem.title,
            summary:agendaItem.summary?<><h3>Summary:</h3><p>{agendaItem.summary}</p></>:<></>,
            ai_summary:agendaItem.ai_summary?<><AiGeneratedContent>{agendaItem.ai_summary}</AiGeneratedContent></>:<></>,
            recommendation:agendaItem.recommendation?<><h3>Recommendation:</h3><p>{agendaItem.recommendation}</p></>:<></>,
            decisionRecommendations: agendaItem.decisionRecommendations?<><h3>Decision Recommendation:</h3><p>{agendaItem.decisionRecommendations}</p></>:<></>,
            decisionAdvice: agendaItem.decisionAdvice?<><h3>Decision Advice:</h3><p>{agendaItem.decisionAdvice}</p></>:<></>,
            reference: agendaItem.reference,
            meetingDate: formatDate(agendaItem.meetingDate)
        }
    })
}




const SearchResults = async ({query}:{query: string}) => {


    let results:ReturnType<typeof getTextResultsJSXMap>|[] = [];
    let total=0, limit=0;


    try {
        const data = await getSearchResults(query);
        total = data.total || 0;
        limit = data.limit || 0;
        const sourceResults = data.results as agendaItem[];
        const highlightedResults = data.highlightedResults as agendaItemHighlights[];
        if(highlightedResults){
            results = getHIghlightedResultsJSXMap(highlightedResults); 
        }
        else{
            results = getTextResultsJSXMap(sourceResults);
        }
        
    }
    catch(err){
        console.log("Search Results Fetch Error:", err);
    }

    return (
        <div className="flex flex-col p-4 md:p-10">
            <div className="flex flex-col w-full">
                {results.length>0 && total > 1 && <div>{(limit>total)?`Found ${total} matches.`:`Showing top ${limit} results.`}</div>}
                {results.length>0 && results.map((agendaItem) => (
                    <div key={agendaItem.reference} className="flex flex-col w-full p-2">
                        <div className="card w-full bg-base-100 shadow-xl">
                            <div className="card-body">
                                <div className="prose w-full">
                                    <h2>{agendaItem.title}</h2>
                                    <div className="flex flex-row gap-3 items-start flex-wrap">
                                        <Chip>{agendaItem.meetingDate}</Chip>
                                        <Chip>{agendaItem.reference}</Chip>
                                        <Chip>{agendaItem.itemStatus}</Chip>
                                    </div>
                                </div>
                                <div className="prose">
                                    {agendaItem.ai_summary}
                                </div>
                                
                                <div className="prose">
                                    <div className="collapse collapse-arrow bg-base-200">
                                        <input type="checkbox" name={`${agendaItem.reference}_details`} className="accordion-toggle" />
                                        <div className="collapse-title text-m font-m underline">Details</div>
                                        <div className="collapse-content">
                                            {agendaItem.recommendation}
                                            {agendaItem.decisionAdvice}
                                            {agendaItem.decisionRecommendations}
                                            {agendaItem.summary}                                        
                                        </div>
                                    </div>
                                </div>
                                <div className="prose">
                                    <p><Link target="_blank" className="inline-block break-words w-full" href={`https://secure.toronto.ca/council/agenda-item.do?item=${agendaItem.reference}`} >
                                        https://secure.toronto.ca/council/agenda-item.do?item={agendaItem.reference}
                                    </Link></p>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
                {results.length==0 && (
                    <div className="flex flex-col w-full p-2">
                        <div className="card w-full bg-base-100 shadow-xl">
                            <div className="card-body">
                                <div className="prose w-full">
                                    <h2>No results found</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>)
}

export default SearchResults;