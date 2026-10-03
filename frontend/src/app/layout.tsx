import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sehat Evidence — Understand the evidence",
  description: "Adult diabetes research and doctor-visit preparation, with inspectable source passages.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
