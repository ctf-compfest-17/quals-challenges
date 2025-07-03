import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";
import Image from 'next/image'
import Logo from "@/public/ferrari/logo.svg";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Gift for the Tifosi",
  description: "A special gift for Ferrari fans"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} bg-[radial-gradient(circle_at_top,#ED1131,#710006)] antialiased`}
      >
        {children}
        <Toaster
          position="top-right"
          richColors
          closeButton
          duration={4000}
        />
        <div className="absolute bottom-8 right-4 w-24 h-24 z-[3]">
          <Image
            src={Logo}
            alt="Logo"
            fill
            className="object-contain invert"
            sizes="96px"
          />
        </div>
      </body>
    </html>
  );
}
