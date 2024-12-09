"use client";

import React, { useState, useRef } from "react";
import { useSearchParams, useRouter, usePathname } from "next/navigation";



/**
 * SearchBar component for handling search functionality. Redirects to Search Results page after search submit.
 * 
 * This component provides a search interface that:
 * - Maintains search query state
 * - Updates URL parameters based on search input
 * - Preserves search state through URL parameters
 * - Provides real-time search term logging
 * 
 * @component
 * @returns {JSX.Element} A form containing a search input and submit button
 */

const SearchBar = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const searchParams = useSearchParams();
    const { push } = useRouter();
    const submitBtnRef = useRef<HTMLButtonElement>(null);
    const pathname = usePathname();

    /**
     * Handles changes to the search input field.
     * Updates the searchQuery state and logs the current search term.
     * 
     * @param {React.ChangeEvent<HTMLInputElement>} e - The change event from the input field
     */
    const handleSearchQuery = (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setSearchQuery(value);
    };

    /**
     * Handles the search form submission.
     * Prevents default form submission, updates URL parameters with the current search query,
     * and navigates to the updated URL.
     * 
     * @param {React.FormEvent<HTMLFormElement>} event - The form submission event
     */
    const handleSearchClick = (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      const params = new URLSearchParams(searchParams);
      if(searchQuery){
        params.set("query", searchQuery);
      }
      else{
        params.delete("query");
      }

      push(`${pathname}?${params.toString()}`);
    };

  return (
    <form onSubmit={handleSearchClick}>
      <div className="flex flex-row items-center">
        <div className="join px-4 py-8 md:p-10 w-screen justify-center">
            <input
              type="text"
              placeholder="Search"
              className="input input-bordered bg-base-100 join-item w-4/5 md:w-3/4 lg:w-1/2"
              onChange={handleSearchQuery}
              defaultValue={searchParams.get("query")?.toString()}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  submitBtnRef.current?.focus();
                }
              }}
            />
            <button ref={submitBtnRef} className="btn btn-primary join-item" type="submit">Search</button>
          </div>
      </div>
    </form>
  );
}


export default SearchBar;