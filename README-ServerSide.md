This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started
### Prerequisites:
Make sure you have the Elasticsearch server running. Follow the instructions in the Elasticsearch server project's README.md to start the server.

### 1. Install dependencies
First install the dependencies:
```bash
npm install
```

### 2. Run the development server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The project starts in the `app/page.tsx`. The page auto-updates as you edit the file.


### 3. Project Structure
The project is a simple NextJS app that allows you to search for agenda items in Elasticsearch.

The project starts in the `app/page.tsx`. Search is implemented in the `app/services/search-client.ts` file. The search is performed using the `search` function, which is a wrapper around the Elasticsearch client's `search` function.

> **Client-Server Separation**
> As a NextJS app, this project can have a server-side component that can replace the 'search' server in the ElasticSearch-Server project. A sample of this implementation is available in the `services/search-server.ts` file.
> Swap out the `SearchResults` component in the `SearchResults.tsx` file with the `serverside-example.tsx` file to see a demonstration of this.

### 4. Building the Project
#### 4.1. Build Only static content
Run the following command to build the project:
```bash
npm run build
```
This will generate an 'out' folder with the production build of the static content of the project. Copy the contents of the 'out' folder to the 'next_build' folder in the Elasticsearch-Server project.

#### 4.2. Build with server-side rendering
Open next.config.mjs and comment the `output:build` option.

```js
//output: 'export',
```

Then run the following command to build the project:
```bash
npm run build
```

This will generate a .next folder containing the production build of the app, including the server-side rendering code.
Run `npm run start` to start the nextjs server, and navigate to `http://localhost:3000/` to see the search page.