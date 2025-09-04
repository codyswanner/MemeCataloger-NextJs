import type { Metadata } from "next";



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
        {children}
      </body>
    </html>
  );
}
