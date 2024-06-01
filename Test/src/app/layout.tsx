import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], display: "swap", });

export const metadata: Metadata = {
  title: "Banking TZone",
  description: "Where magic begins slowly in banking.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <body className="bg-background text-foreground">
        <main className="min-h-screen flex flex-col items-center font-outfit">
          {children}
        </main>
      </body>
    </html>
  );
}
