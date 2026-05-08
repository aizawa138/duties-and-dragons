import Card from "@/src/components/ui/card/card";
import knight from "@/public/knight.png";
import mage from "@/public/mage.png";
import vampire from "@/public/vampire.png";
import Header from "@/src/components/header/Header";

export default function Page() {
  return (
    <>
      <Header />
      <div
        className={`inline-flex justify-center items-center min-h-[calc(100vh-64px)] w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden`}
      >
        <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
        <div className="bg-background px-6 py-10 rounded-2xl border border-accent">
          <h1 className="text-3xl text-foreground mb-8 text-center font-bold">
            Which classes do you want to be?
          </h1>
          <div className="flex gap-4">
            <Card src={knight} role="Knight" />
            <Card src={mage} role="Mage" />
            <Card src={vampire} role="Vampire" />
          </div>
        </div>
      </div>
    </>
  );
}
