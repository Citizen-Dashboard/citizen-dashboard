<!-- src/components/SearchBar.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
    let searchTerm = '';
  
    function handleInput() {
      dispatch('search', searchTerm);
    }
  </script>
  
  <div class="search-bar">
    <input
      type="text"
      bind:value={searchTerm}
      on:input={handleInput}
      placeholder="Search..."
    />
  </div>
  
  <style>
    .search-bar {
      margin-bottom: 1em;
    }
    input {
      width: 100%;
      padding: 0.5em;
      font-size: 1em;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  </style>
  