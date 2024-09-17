/** @type {import('next').NextConfig} */
const nextConfig = {
    /* Configure Nextjs app to run as a client side app, not a server side app. */
    output: 'export',   //comment this if you want to render the app on the server side and use serve side fetch of search results.
    rewrites: async () => {
        return [
            {
                source: '/search/:path*',
                destination: process.env.NEXT_PUBLIC_elasticSearchServer + '/:path*',
            },
        ];
    },
};

export default nextConfig;
