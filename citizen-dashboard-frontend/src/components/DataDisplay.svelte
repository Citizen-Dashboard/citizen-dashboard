<script>
    import { onMount } from 'svelte';
    import DataRow from './DataRow.svelte';
    import SearchBar from './SearchBar.svelte';

    let data = [];
    let filteredData = [];

    async function fetchData() {
        const response = await fetch('http://localhost:5000/search?term=');
        const result = await response.json();
        data = result;
        filteredData = result;
    }

    onMount(() => {
        fetchData();
    });

    function handleSearch(event) {
        const searchTerm = event.detail.toLowerCase();
        filteredData = data.filter(item =>
            item.title.toLowerCase().includes(searchTerm) ||
            item.summary.toLowerCase().includes(searchTerm)
        );
    }
</script>

<div class="data-display">
    <SearchBar on:search={handleSearch} />

    <div class="data-list">
        {#each filteredData as item (item.id)}
            <DataRow {item} />
        {/each}
    </div>
</div>

<style>
    .data-display {
        max-width: 600px;
        margin: 0 auto;
    }
    .data-list {
        display: flex;
        flex-direction: column;
        gap: 1em;
    }
</style>