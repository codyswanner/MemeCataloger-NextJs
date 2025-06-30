import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: ['localhost', '127.0.0.1'],
  images: {
    remotePatterns: [new URL('http://backend:8000/media/**')]
  }
};

export default nextConfig;
