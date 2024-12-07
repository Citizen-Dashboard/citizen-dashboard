'use client'
import Link from "next/link";
import  {getSearchResults} from '@/services/search-client'
import { useEffect, useState } from "react";

/**
 * Client-side Search Results component that displays agenda items based on a search query.
 * 
 * This component:
 * - Fetches search results client-side using the provided query
 * - Manages search results state using React hooks
 * - Re-fetches results when the search query changes
 * - Renders a list of agenda items with their details
 * - Displays title, status, decision body, advice, recommendations and summary for each item
 * - Provides links to the full agenda items on toronto.ca
 * - Handles errors gracefully by logging them to console
 * 
 * @component
 * @param {Object} props - Component props
 * @param {string} props.query - The search query string to filter agenda items
 * @returns {JSX.Element} The rendered search results
 */

const SearchResults = ({query}:{query: string}) => {

    const [results, setResults] = useState<agendaItem[]>([]);

    useEffect(() => {
        getSearchResults(query)
        .then((data) => {
            const searchResults:agendaItem[] = data.results as agendaItem[];
            setResults(searchResults);
        })
        .catch((error) => {
            console.error(error);
        });
    }, [query]);

    return (
        <div className="flex flex-col p-10">
            <div className="flex flex-col w-full">
                {results.map((agendaItem:agendaItem) => (
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
            </div>
        </div>)
}

export default SearchResults;