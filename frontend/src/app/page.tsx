"use client";

import { useEffect } from "react";
import Header from "../components/header/Header";
import MainInfo from "../components/landing-info/main-info";
import { initializeApp } from "@/lib/initializeApp";

export default function Home() {
  useEffect(() => {
    initializeApp();
  }, []);

  return (
    <main className="relative">
      <Header />
      <MainInfo />
    </main>
  );
}
