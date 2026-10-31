import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    id: "/",
    name: "Teilbar",
    short_name: "Teilbar",
    description: "Nachbarn statt Fremde: Tiersitting und Housesitting unter Nachbarn",
    lang: "de",
    start_url: "/",
    scope: "/",
    display: "standalone",
    background_color: "#F2F9F4",
    theme_color: "#1B6B3A",
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icons/icon-maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
