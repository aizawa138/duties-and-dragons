import { alikeAngular } from "@/public/fonts";
import Player from "../player/player";
import Enemy from "../enemy/enemy";
import Tabs from "../tabs/tabs";

export default function DashboardBack() {
    return (
        <div className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}>
            <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
            <div className="w-3/4 h-screen bg-black border-r-4 border-l-4 border-primary">
                <div className="flex flex-row justify-between">
                    <div className="pl-10 pt-10 flex flex-col w-1/3">
                        <Player />
                        <Tabs />
                    </div>
                    <div className="flex flex-col w-1/3" />
                    <div className="pr-10 pt-10 flex flex-col w-1/3">
                        <Enemy />
                    </div>
                </div>
            </div>
        </div>
    )
}