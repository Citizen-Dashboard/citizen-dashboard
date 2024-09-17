import AppBar from "@/app/AppBar";
import SearchBar from "@/app/SearchBar";
import SearchResults from "@/app/SearchResults";



export default async function Home(
  {searchParams}: {searchParams: {query: string}}
) {
  const query = searchParams?.query|| '';

  return (
    <div>
      <AppBar />
      <SearchBar />
      <SearchResults query={query} />
    </div>
  );
}
