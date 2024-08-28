<script>
    import { onMount } from 'svelte';
    import DataRow from './DataRow.svelte';
    import SearchBar from './SearchBar.svelte';

    let data = [];

    async function fetchData(searchTerm) {
        const response = await fetch(`http://localhost:${import.meta.env.VITE_SEARCH_API_PORT}/search?term=${searchTerm}`);
        const result = await response.json();
        data = result;
    }

    function handleSearch(event) {
        const searchTerm = event.detail;
        fetchData(searchTerm);
    }
</script>

<div class="data-display">
    <SearchBar on:search={handleSearch} />

    <div class="data-list">
        {#each data as item}
            <DataRow {item} />
        {/each}
    </div>
</div>