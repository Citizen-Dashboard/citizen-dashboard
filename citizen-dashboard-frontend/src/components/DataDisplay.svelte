<!-- src/components/DataDisplay.svelte -->
<script>
    import { onMount } from 'svelte';
    import DataRow from './DataRow.svelte';
    import SearchBar from './SearchBar.svelte';
  
    let data = [];
    let filteredData = [];
  
    onMount(() => {
      // Simulate fetching data from an API with mock data
      const mockData = [
        { id: 1, name: 'John Doe', value: 'Sample Data 1' },
        { id: 2, name: 'Jane Smith', value: 'Sample Data 2' },
        { id: 3, name: 'Alice Johnson', value: 'Sample Data 3' },
        // Add more mock data as needed
      ];
  
      data = mockData;
      filteredData = mockData;
    });
  
    function handleSearch(event) {
      const searchTerm = event.detail.toLowerCase();
      filteredData = data.filter(item =>
        item.name.toLowerCase().includes(searchTerm) ||
        item.value.toLowerCase().includes(searchTerm)
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
  