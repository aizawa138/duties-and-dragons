import type { Metadata } from "next";
import { alikeAngular } from "@/public/fonts";
import "../../styles/globals.css";

export const metadata: Metadata = {
  title: "Duties and Dragons",
  description: "Enables productive task management with the collaboration with gaming",
};

export default function DashboardLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return (
      <section className="dashboard-container">
        {children} 
      </section>
    );
}
