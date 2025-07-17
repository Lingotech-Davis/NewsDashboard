import type { Metadata } from "next";
// import { Inter } from "next/font/google";
// import Nav from "@/components/nav";
import '@/styles/globals.css'

// const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "News Dashboard",
  description: "Prototype for news dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="main">
          <div className="gradient" />
        </div>

        <div className="flex flex-col h-full">
          {/* <Nav /> */}
          <div className="app flex-grow">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
