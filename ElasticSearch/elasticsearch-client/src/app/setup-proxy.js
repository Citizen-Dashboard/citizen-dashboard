import createProxyMiddleware from 'http-proxy-middleware';

export default function setupProxy(app) {
    app.use('/search', createProxyMiddleware({
        target: process.env.NEXT_PUBLIC_elasticSearchServer,
        changeOrigin: true,
    }));
}