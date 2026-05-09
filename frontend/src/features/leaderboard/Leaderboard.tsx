"use client";

import backendUrl from "@/lib/backendUrl";
import { alikeAngular, crossaintOne } from "@/public/fonts";
import { useEffect, useState } from "react";

type RankingData = {
  username: string;
  level: number;
  exp: number;
};

type LeaderboardResponse = {
  leaderboard?: RankingData[];
};

export default function Leaderboard() {
  const [rankingData, setRankingData] = useState<RankingData[]>([]);

  useEffect(() => {
    const handleLeaderboard = async () => {
      try {
        const response = await fetch(backendUrl("/api/leaderboard/"));

        if (!response.ok) {
          setRankingData([]);
          return;
        }

        const data = (await response.json()) as LeaderboardResponse;
        setRankingData(Array.isArray(data.leaderboard) ? data.leaderboard : []);
      } catch (error) {
        console.error("Failed to fetch leaderboard", error);
        setRankingData([]);
      }
    };
    handleLeaderboard();
  }, []);
  return (
    <div
      className={`w-full h-full max-w-sm mx-auto rounded-lg border border-slate-800 bg-slate-950/90 p-3 shadow-2xl shadow-slate-950/50 backdrop-blur-xl ${alikeAngular.className}`}
    >
      <h1
        className={`text-xl font-bold mb-2 text-accent text-center ${crossaintOne.className}`}
      >
        Leaderboard
      </h1>
      <p className="text-secondary mb-3 text-xs text-center">
        Top players and their ranks.
      </p>

      <div className="space-y-2">
        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2">
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">
            Rank
          </span>
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">
            Player
          </span>
        </div>

        {rankingData.map((data, i) => (
          <div
            key={data.username}
            className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2"
          >
            <span className="font-semibold text-sm text-accent">{i + 1}</span>
            <span className="font-medium text-accent text-xs">
              {data.username}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
