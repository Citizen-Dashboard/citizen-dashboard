<script>
    import DataDisplay from '../components/DataDisplay.svelte';
  </script>
  
  <svelte:head>
    <title>Citizen Dashboard</title>
  </svelte:head>
  
  <main>
    <h1>Citizen Dashboard</h1>
    <DataDisplay />
  </main>
  
  <style>
    main {
      padding: 1rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    h1 {
      font-size: 2rem;
      text-align: center;
      margin-bottom: 1rem;
    }
  </style>
  