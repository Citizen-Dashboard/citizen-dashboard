"use client";

import AppBar from "@/app/AppBar";
import SearchBar from "@/app/SearchBar";
import SearchResults from "@/app/SearchResults";
import { useSearchParams } from "next/navigation";
import { Suspense } from 'react'



function Home() {
  const query = useSearchParams().get("query")||"";

  return (
    <div>
      <AppBar />
      <SearchBar />
      <Suspense fallback={<div>Loading...</div>}>
        <SearchResults query={query} />
      </Suspense>
    </div>
  );
}


export default function HomePage(){
  return (
      <Home />
  );
};
