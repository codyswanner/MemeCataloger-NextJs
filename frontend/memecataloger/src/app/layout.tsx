import type { Metadata } from "next";
import "./_styles/globals.css"

import Header from "./_components/Header";


export const metadata: Metadata = {
  title: "MemeCataloger",
  description: "I heard you liked memes, so I put some memes in your memes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.jpg" />
      </head>
      <body>
          <Header />
          {children}
      </body>
    </html>
  );
};
