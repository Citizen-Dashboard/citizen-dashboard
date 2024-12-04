/** @type {import('next').NextConfig} */
const nextConfig = {
    /* Uncomment below line to configure Nextjs app to run as a client side app, not a server side app. */
    /* output: 'export', */
    rewrites: async () => {
        return [
            {
                source: '/search/:path*',
                destination: process.env.NEXT_PUBLIC_elasticSearchServer + '/:path*',
            },
        ];
    }
};

export default nextConfig;
