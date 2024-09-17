'use client'
import Link from "next/link";
import  {getSearchResults} from '@/services/search-client'
import { useEffect, useState } from "react";


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