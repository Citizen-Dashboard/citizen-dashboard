//this will be rendered server side.

import Link from "next/link";

/** 
 * Use @/services/search-elastic to connect to Elasticsearch
 * Use @/services/search-opensearch to connect to AWS OpenSearch
 */
// import  {getSearchResults} from '@/services/search-elastic'
import  {getSearchResults} from '@/services/search-opensearch'

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

const SearchResults = async ({query}:{query: string}) => {

    let results:agendaItem[]|[] = [];
    try {
        const data = await getSearchResults(query);
        results = data.results as agendaItem[];
    }
    catch(err){
        console.log("Search Results Fetch Error:", err);
    }

    return (
        <div className="flex flex-col p-10">
            <div className="flex flex-col w-full">
                {results.length>0 && results.map((agendaItem:agendaItem) => (
                    <div key={agendaItem.reference} className="flex flex-col w-full p-2">
                        <div className="card w-full bg-base-100 shadow-xl">
                            <div className="card-body collapse collapse-arrow">
                                <div className="prose w-full">
                                    <h2>{agendaItem.title}</h2>
                                    {agendaItem.itemStatus && <p>{agendaItem.itemStatus}</p>}
                                    {agendaItem.decisionBodyName && <p>{agendaItem.decisionBodyName}</p>}
                                </div>
                                <div className="prose">
                                    {agendaItem.decisionAdvice && <p>{agendaItem.decisionAdvice}</p>}
                                    {agendaItem.decisionRecommendations && <p>{agendaItem.decisionRecommendations}</p>}
                                    {agendaItem.summary && <p>{agendaItem.summary}</p>}
                                </div>
                                <div className="prose">
                                    <p><Link href={`https://secure.toronto.ca/council/agenda-item.do?item=${agendaItem.reference}`} >
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