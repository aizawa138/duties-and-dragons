import type { Metadata } from "next";
import { alikeAngular } from "@/public/fonts";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Duties & Dragons",
  description:
    "Enables productive task management with the collaboration with gaming",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`h-full`}>
      <body className={`${alikeAngular.className} min-h-full flex flex-col`}>
        {children}
      </body>
    </html>
  );
}
