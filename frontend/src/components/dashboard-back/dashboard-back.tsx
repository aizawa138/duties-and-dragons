"use client";

import React, { useState } from "react";
import { alikeAngular } from "@/public/fonts";
import Player from "../player/player";
import Enemy from "../enemy/enemy";
import Tabs from "../tabs/tabs";
import Leaderboard from "@/src/features/leaderboard/Leaderboard";
import AttackButton from "../attack-button/attack-button";

// Define the type here so it's accessible
interface ListItem {
  id: number;
  text: string;
  completed: boolean;
  deadline?: string;
}

export default function DashboardBack() {
    // 1. Move state here from Tabs.tsx
    const [tasks, setTasks] = useState<ListItem[]>([]);
    const [habits, setHabits] = useState<ListItem[]>([]);

    // 2. Create the attack logic
    const handleAttack = () => {
        // Filter out completed duties (tasks), keep everything else
        setTasks(prev => prev.filter(task => !task.completed));
        console.log("Attack! Completed duties cleared.");
    };

    return (
        <div className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}>
            <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
            
            <div className="w-3/4 min-h-screen border-r border-l border-slate-800 bg-slate-950/40 backdrop-blur-md shadow-2xl p-10">
                <div className="grid grid-cols-7 gap-10 w-full h-full items-stretch">
                    <div className="col-span-1">
                        <Player s="some stats."/>
                    </div>
                    <div className="col-span-2">
                        <Player s="a Player image."/>
                    </div>
                    
                    <div className="col-span-1">
                        {/* 3. Pass the function to the button */}
                        <AttackButton onAttack={handleAttack} />
                    </div>

                    <div className="col-span-2">
                        <Enemy s="an Enemy image."/>
                    </div>

                    <div className="col-span-1">
                        <Enemy s="some stats."/>
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