"use client";

import AppBar from "@/app/AppBar";
import Loading from "@/app/Loading";
import SearchBar from "@/app/SearchBar";
import SearchResults from "@/app/SearchResults/ClientsideResults";
import { useSearchParams } from "next/navigation";
import { Suspense } from 'react'


/**
 * Client-side HomePage implementation that uses an independent search API for retrieving results.
 * 
 * This module implements a completely client-side NextJS application that:
 * - Makes API calls to a separate server-side search service
 * - Can be deployed as a static site since all data fetching happens client-side
 * - Uses Next.js client components for dynamic search functionality
 * - Implements suspense boundaries for loading states
 * 
 * The search flow:
 * 1. User enters search query
 * 2. Client makes request to separate search API endpoint
 * 3. Search API queries ElasticSearch/OpenSearch and returns results
 * 4. Results are rendered client-side
 * 
 * This differs from the server-side implementation which directly queries 
 * the search backend from Next.js server components.
 * 
 * @module HomePage/client-page
 */

function Home() {
  const query = useSearchParams().get("query")||"";

  return (
    <div>
      <AppBar />
      <SearchBar />
      {query!=="" &&
        <Suspense key={query} fallback={<Loading />}>
          <SearchResults query={query} />
        </Suspense>
      }
    </div>
  );
}


export default function HomePage(){
  return (
      <Home />
  );
};
