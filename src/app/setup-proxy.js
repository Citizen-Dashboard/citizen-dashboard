/**
 * @module setup-proxy
 * @description Configures proxy middleware for the application to forward search requests
 * to the Elasticsearch/OpenSearch server. This enables client-side search functionality
 * while avoiding CORS issues.
 * 
 * @requires http-proxy-middleware
 * 
 * @example
 * // In your app's setup:
 * import setupProxy from './setup-proxy';
 * setupProxy(app);
 */



import createProxyMiddleware from 'http-proxy-middleware';

export default function setupProxy(app) {
    app.use('/search', createProxyMiddleware({
        target: process.env.NEXT_PUBLIC_elasticSearchServer,
        changeOrigin: true,
    }));
}