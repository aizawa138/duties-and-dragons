"use client";

import Card from "@/src/components/ui/card/card";
import knight from "@/public/knight.png";
import mage from "@/public/mage.png";
import vampire from "@/public/vampire.png";
import Header from "@/src/components/header/Header";
import { Button } from "@/src/components/ui/button/button";
import { usePathname } from "next/navigation";
import { useState } from "react";
import getCookie from "@/lib/getCookie";
import { useRouter } from "next/navigation";
import { initializeApp } from "@/lib/initializeApp";
import backendUrl from "@/lib/backendUrl";

export default function Page() {
  const [role, setRole] = useState("");
  const router = useRouter();

  const pathname = usePathname();
  const username = pathname.split("/")[2];

  const handleClick = (value: string) => {
    setRole(value);
  };

  const handleRoleClick = async () => {
    await initializeApp();
    const csrfToken = getCookie("csrftoken") ?? "";
    const response = await fetch(backendUrl("/api/choose_class/"), {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ user_class: role }),
    });

    if (!response.ok) {
      return;
    }

    router.push(`/dashboard/${username}`);
  };

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
          <div className="flex gap-4 mb-4">
            <Card
              src={knight}
              role="Knight"
              onClick={handleClick}
              isSelected={role === "Knight"}
              description="Good morning"
            />
            <Card
              src={mage}
              role="Mage"
              onClick={handleClick}
              isSelected={role === "Mage"}
              description="Good night"
            />
            <Card
              src={vampire}
              role="Vampire"
              onClick={handleClick}
              isSelected={role === "Vampire"}
              description="Hi"
            />
          </div>
          <div className="flex justify-end mr-4">
            <Button variant="secondary" size="lg" onClick={handleRoleClick}>
              Create
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
