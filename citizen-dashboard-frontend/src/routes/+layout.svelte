<script>
    import Header from './Header.svelte';
    import '../app.css';
  </script>
  
  <Header />
  
  <main>
    <slot />
  </main>
  
  <footer>
    <p>© 2024 Citizen Dashboard</p>
  </footer>
  
  <style>
    main {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 1rem;
      width: 100%;
      max-width: 1024px;
      margin: 0 auto;
      box-sizing: border-box;
    }
  
    footer {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }
  </style>
  