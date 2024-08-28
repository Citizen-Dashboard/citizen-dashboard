<header>
    <div class="corner">
      <!-- Add your logo here if you have one -->
    </div>
  
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <!-- Add more navigation items as needed -->
      </ul>
    </nav>
  
    <div class="corner">
      <!-- Add any corner content (e.g., user profile) -->
    </div>
  </header>
  
  <style>
    header {
      display: flex;
      justify-content: space-between;
    }
  
    .corner {
      width: 3em;
      height: 3em;
    }
  
    nav {
      display: flex;
      justify-content: center;
      --background: rgba(255, 255, 255, 0.7);
    }
  
    ul {
      position: relative;
      padding: 0;
      margin: 0;
      height: 3em;
      display: flex;
      justify-content: center;
      align-items: center;
      list-style: none;
      background: var(--background);
      background-size: contain;
    }
  
    li {
      position: relative;
      height: 100%;
    }
  
    nav a {
      display: flex;
      height: 100%;
      align-items: center;
      padding: 0 1em;
      color: var(--color-text);
      font-weight: 700;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      text-decoration: none;
      transition: color 0.2s linear;
    }
  </style>
  