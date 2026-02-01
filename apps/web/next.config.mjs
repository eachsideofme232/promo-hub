/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@promohub/types', '@promohub/ui', '@promohub/utils'],
}

export default nextConfig
