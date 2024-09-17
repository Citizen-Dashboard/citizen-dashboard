"use client";
import React, { useState } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";


const SearchBar = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const searchParams = useSearchParams();
    const {replace} = useRouter();
    const pathname = usePathname();


    const handleSearchQuery = (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setSearchQuery(value);
      console.log("Search term:", value);
    };

    const handleSearchClick = (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      const params = new URLSearchParams(searchParams);
      if(searchQuery){
        params.set("query", searchQuery);
      }
      else{
        params.delete("query");
      }

      replace(`${pathname}?${params.toString()}`);
    };

  return (
    <form onSubmit={handleSearchClick}>
      <div className="flex flex-row items-center">
        <div className="join p-10 w-screen justify-center">
            <input
              type="text"
              placeholder="Search"
              className="input bg-base-300 join-item w-1/2"
              onChange={handleSearchQuery}
              defaultValue={searchParams.get("query")?.toString()}
            />
            <button className="btn btn-primary join-item" type="submit">Search</button>
          </div>
      </div>
    </form>
  );
}


export default SearchBar;