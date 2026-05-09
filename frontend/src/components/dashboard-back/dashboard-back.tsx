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
import { initializeApp } from "@/lib/initializeApp";

// Define the type here so it's accessible
interface ListItem {
  id: number;
  text: string;
  strength: number;
  intelligence: number;
  charisma: number;
  completed: boolean;
  deadline?: string;
}

interface DashboardDuty {
  duty_id: number;
  description: string;
  strength?: number | null;
  intelligence?: number | null;
  charisma?: number | null;
  status: string;
  deadline?: string;
}

interface DashboardHabit {
  habit_id: number;
  description: string;
  strength?: number | null;
  intelligence?: number | null;
  charisma?: number | null;
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
    strength: Number(duty.strength ?? 0),
    intelligence: Number(duty.intelligence ?? 0),
    charisma: Number(duty.charisma ?? 0),
    completed: duty.status === "Completed",
    deadline: duty.deadline,
  }));

const mapHabits = (habits: DashboardHabit[] = []): ListItem[] =>
  habits.map((habit) => ({
    id: habit.habit_id,
    text: habit.description,
    strength: Number(habit.strength ?? 0),
    intelligence: Number(habit.intelligence ?? 0),
    charisma: Number(habit.charisma ?? 0),
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
  const [bossInfo] = useState<BossInfo | null>(null);

  const [strength, setStrength] = useState(0);
  const [intelligence, setIntelligence] = useState(0);
  const [charisma, setCharisma] = useState(0);

  // 2. Create the attack logic
  const handleAttack = async () => {
    // Filter out completed duties (tasks), keep everything else
    const csrfToken = await initializeApp();
    const response = await fetch(backendUrl("/api/attack_boss/"), {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    });
    const data = await response.json();
    setStrength(data.stats.strength);
    setIntelligence(data.stats.inteligence);
    setCharisma(data.stats.charisma);

    setTasks((prev) => prev.filter((task) => !task.completed));
    setShake(true);

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
      setStrength(data.status.strength);
      setIntelligence(data.status.intelligence);
      setCharisma(data.status.charisma);
      setTasks(mapDuties(data.duties));
      setHabits(mapHabits(data.habits));
    };
    fetchData();
  }, [initialUserInfo]);
  console.log(bossInfo);

  return (
    <div
      className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}
    >
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />

      <div className="w-3/4 min-h-screen border-r border-l border-slate-800 bg-slate-950/40 backdrop-blur-md shadow-2xl p-10">
        <div className="grid grid-cols-7 gap-4 w-full h-full items-stretch">
          <div className="col-span-1">
            <PlayerStats
              str={
                strength === 0
                  ? userInfo?.strength
                    ? userInfo.strength
                    : 0
                  : strength
              }
              int={
                intelligence === 0
                  ? userInfo?.intelligence
                    ? userInfo?.intelligence
                    : 0
                  : intelligence
              }
              cha={
                charisma === 0
                  ? userInfo?.charisma
                    ? userInfo?.charisma
                    : 0
                  : charisma
              }
              hp={userInfo?.user_hp ? userInfo?.user_hp : 0}
            />
          </div>
          <div className="col-span-2">
            <Player
              classname={userInfo?.user_class ? userInfo?.user_class : ""}
              username={userInfo?.username ? userInfo?.username : "Player"}
            />
          </div>

          <div className="flex items-center col-span-1 align-middle">
            {/* 3. Pass the function to the button */}
            <AttackButton onAttack={handleAttack} />
          </div>

          <div className={`col-span-2 ${shake ? "animate-shake" : ""}`} onAnimationEnd={() => setShake(false)}>
            <Enemy s={bossInfo?.boss_id ? bossInfo?.boss_id : 1}/>
          </div>

          <div className="col-span-1">
            <EnemyStats hp={bossInfo?.current_boss_hp ? bossInfo?.current_boss_hp : 0} id={bossInfo?.boss_id ? bossInfo?.boss_id : 1} time_left={bossInfo?.seconds_left ? bossInfo?.seconds_left : 1} />
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
