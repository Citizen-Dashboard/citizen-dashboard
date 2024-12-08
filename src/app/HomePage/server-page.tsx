import AppBar from "@/app/AppBar";
import Loading from "@/app/Loading";
import SearchBar from "@/app/SearchBar";
import SearchResults from "@/app/SearchResults/ServersideResults";
import { Suspense } from "react";


/**
 * Server-side HomePage implementation that directly interfaces with search backends.
 * 
 * This module implements a full-stack NextJS application that:
 * - Uses Next.js server components to directly query ElasticSearch/OpenSearch clusters
 * - Requires server-side rendering since data fetching happens on the server
 * - Provides better security by keeping search credentials server-side
 * - Reduces client-server round trips by fetching data during server render
 * 
 * The search flow:
 * 1. User enters search query
 * 2. Next.js server component receives the query
 * 3. Server component directly queries ElasticSearch/OpenSearch cluster
 * 4. Results are rendered server-side and sent as HTML
 * 
 * This differs from client-side implementations which require a separate
 * search API endpoint and expose more of the search infrastructure to the client.
 * 
 * @module HomePage/server-page
 */

export default async function Home(
  {searchParams}: {searchParams: {query: string}}
) {
  const query = searchParams?.query|| '';

  return (
    <div className="bg-base-200 min-h-full">
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
