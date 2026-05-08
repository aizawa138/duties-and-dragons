import { alikeAngular } from "@/public/fonts";
import Player from "../player/player";
import Enemy from "../enemy/enemy";
import Tabs from "../tabs/tabs";
import Leaderboard from "@/src/features/leaderboard/Leaderboard";

export default function DashboardBack() {
    return (
        <div className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}>
            <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
            
            <div className="w-3/4 min-h-screen border-r border-l border-slate-800 bg-slate-950/40 backdrop-blur-md shadow-2xl p-10">
                {/* 3-Column Grid Layout */}
                <div className="grid grid-cols-6 gap-10 w-full h-full items-stretch">
                    
                    {/* --- ROW 1 --- */}
                    <div className="col-span-3">
                        <Player />
                    </div>
                    {/* Empty center column to keep Player and Enemy separated */}
                    <div className="col-span-3">
                        <Enemy />
                    </div>

                    {/* --- ROW 2 --- */}
                    {/* Tabs span 2 columns to become wider */}
                    <div className="col-span-4">
                        <Tabs />
                    </div>
                    {/* Leaderboard takes the remaining 1 column */}
                    <div className="col-span-2">
                        <Leaderboard />
                    </div>
                    
                </div>
            </div>
        </div>
    )
}