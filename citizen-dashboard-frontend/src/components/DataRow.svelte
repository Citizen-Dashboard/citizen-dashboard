<!-- src/components/DataRow.svelte -->
<script>
    export let item;
  </script>
  
  <div class="data-row">
    <h3>{item.name}</h3>
    <p>{item.value}</p>
  </div>
  
  <style>
    .data-row {
      border: 1px solid #ccc;
      padding: 1em;
      border-radius: 4px;
      background-color: #f9f9f9;
    }
    h3 {
      margin: 0 0 0.5em 0;
    }
    p {
      margin: 0;
    }
  </style>
  