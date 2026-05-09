"use client";

import { alikeAngular } from "@/public/fonts";
import backendUrl from "@/lib/backendUrl";
import Header from "@/src/components/header/Header";
import DashboardBack, { type DashboardUserInfo } from "./dashboard-back";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

type ProtectedDashboardProps = {
  username?: string;
};

function DashboardLoading() {
  return (
    <main
      className={`flex min-h-screen w-full items-center justify-center bg-[#020617] text-slate-200 ${alikeAngular.className}`}
    >
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
      <p className="relative text-sm text-slate-400">Loading...</p>
    </main>
  );
}

export default function ProtectedDashboard({ username }: ProtectedDashboardProps) {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState<DashboardUserInfo | null>(null);

  useEffect(() => {
    let isMounted = true;

    const verifySession = async () => {
      try {
        const response = await fetch(backendUrl("/api/get_user_info/"), {
          method: "GET",
          credentials: "include",
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error("Unauthorized");
        }

        const data = (await response.json()) as DashboardUserInfo;

        if (!isMounted) {
          return;
        }

        if (!data.has_class) {
          router.replace(`/create/${data.username}`);
          return;
        }

        if (!username) {
          router.replace(`/dashboard/${data.username}`);
          return;
        }

        if (data.username !== username) {
          router.replace(`/dashboard/${data.username}`);
          return;
        }

        setUserInfo(data);
      } catch {
        if (isMounted) {
          router.replace("/");
        }
      }
    };

    void verifySession();

    return () => {
      isMounted = false;
    };
  }, [router, username]);

  if (!userInfo) {
    return <DashboardLoading />;
  }

  return (
    <>
      <main className="relative">
        <Header
          initialAuthUser={{
            username: userInfo.username,
            has_class: userInfo.has_class,
          }}
        />
        <DashboardBack initialUserInfo={userInfo} />
      </main>
    </>
  );
}
