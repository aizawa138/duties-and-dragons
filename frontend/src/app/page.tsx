import { Main } from "next/document";
import Header from "../components/header/Header";
import MainInfo from "../components/landing-info/main-info";

export default function Home() {
  return (
    <main className="relative">
      <Header />
      <MainInfo />
    </main>
  );
}
