
/**
 * This app can be implemented in two ways:
 * 
 * 1. Client-side only (HomePage/client-page):
 *    - NextJS runs as a static site
 *    - Makes API calls to a separate search service
 * 
 * 2. Full-stack (HomePage/server-page):
 *    - NextJS handles both client and server
 *    - Talks directly to search databases
 *    - Requires server-side rendering
 */

// import HomePage from "./HomePage/client-page";
import HomePage from "./HomePage/server-page";
export default HomePage;