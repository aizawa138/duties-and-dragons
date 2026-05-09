"use client";

import React, { useEffect, useState } from "react";
import { alikeAngular } from "@/public/fonts";
import Player from "../player/player";
import Enemy from "../enemy/enemy";
import Tabs from "../tabs/tabs";
import Leaderboard from "@/src/features/leaderboard/Leaderboard";
import AttackButton from "../attack-button/attack-button";
import backendUrl from "@/lib/backendUrl";
// import { initializeApp } from "@/lib/initializeApp";
// import getCookie from "@/lib/getCookie";
// import { usePathname } from "next/navigation";
import PlayerStats from "../stats_display/p-stats-display";
import EnemyStats from "../stats_display/e-stats-display";

// Define the type here so it's accessible
interface ListItem {
  id: number;
  text: string;
  completed: boolean;
  deadline?: string;
}

interface DashboardDuty {
  duty_id: number;
  description: string;
  status: string;
  deadline?: string;
}

interface DashboardHabit {
  habit_id: number;
  description: string;
  status: string;
}

export interface DashboardUserInfo {
  user_id: number;
  username: string;
  user_class: string;
  has_class: boolean;
  level: number;
  strength: number;
  intelligence: number;
  charisma: number;
  user_hp: number;
  duties: DashboardDuty[];
  habits: DashboardHabit[];
  current_fight: null | BossInfo;
}

interface BossInfo {
  fight_id: number;
  user_id: number;
  boss_id: number;
  seconds_left: number;
  current_boss_hp: number;
}

type DashboardBackProps = {
  initialUserInfo?: DashboardUserInfo;
};

const mapDuties = (duties: DashboardDuty[] = []): ListItem[] =>
  duties.map((duty) => ({
    id: duty.duty_id,
    text: duty.description,
    completed: duty.status === "Completed",
    deadline: duty.deadline,
  }));

const mapHabits = (habits: DashboardHabit[] = []): ListItem[] =>
  habits.map((habit) => ({
    id: habit.habit_id,
    text: habit.description,
    completed: habit.status === "Completed",
  }));

export default function DashboardBack({ initialUserInfo }: DashboardBackProps) {
  // 1. Move state here from Tabs.tsx
  const [tasks, setTasks] = useState<ListItem[]>(() =>
    mapDuties(initialUserInfo?.duties),
  );
  const [habits, setHabits] = useState<ListItem[]>(() =>
    mapHabits(initialUserInfo?.habits),
  );
  const [userInfo, setUserInfo] = useState<DashboardUserInfo | undefined>(
    initialUserInfo,
  );
  const [bossInfo, setBossInfo] = useState<BossInfo | null>(null);

  // 2. Create the attack logic
  const handleAttack = () => {
    // Filter out completed duties (tasks), keep everything else
    setTasks((prev) => prev.filter((task) => !task.completed));
    console.log("Attack! Completed duties cleared.");
  };

  useEffect(() => {
    if (initialUserInfo) {
      return;
    }

    const fetchData = async () => {
      const response = await fetch(backendUrl("/api/get_user_info/"), {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });

      if (!response.ok) {
        console.error("Failed to fetch dashboard data", response.status);
        return;
      }

      const data = await response.json();
      setUserInfo(data);
      setTasks(mapDuties(data.duties));
      setHabits(mapHabits(data.habits));
    };
    fetchData();
  }, [initialUserInfo]);

  return (
    <div
      className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}
    >
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />

      <div className="w-3/4 min-h-screen border-r border-l border-slate-800 bg-slate-950/40 backdrop-blur-md shadow-2xl p-10">
        <div className="grid grid-cols-7 gap-4 w-full h-full items-stretch">
          <div className="col-span-1">
            <PlayerStats
              str={userInfo?.strength ? userInfo?.strength : 0}
              int={userInfo?.intelligence ? userInfo?.intelligence : 0}
              cha={userInfo?.charisma ? userInfo?.charisma : 0}
              hp={userInfo?.user_hp ? userInfo?.user_hp : 0}
            />
          </div>
          <div className="col-span-2">
            <Player s={userInfo?.user_class ? userInfo?.user_class : ""} />
          </div>

          <div className="flex items-center col-span-1 align-middle">
            {/* 3. Pass the function to the button */}
            <AttackButton onAttack={handleAttack} />
          </div>

          <div className="col-span-2">
            <Enemy s={bossInfo?.boss_id ? bossInfo?.boss_id : 1} />
          </div>

          <div className="col-span-1">
            <EnemyStats hp={100} weakness="STR" />
          </div>

          <div className="col-span-5">
            {/* 4. Pass state and setters to Tabs */}
            <Tabs
              tasks={tasks}
              setTasks={setTasks}
              habits={habits}
              setHabits={setHabits}
            />
          </div>

          <div className="col-span-2">
            <Leaderboard />
          </div>
        </div>
      </div>
    </div>
  );
}
