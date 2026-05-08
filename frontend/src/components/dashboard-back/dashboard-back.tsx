import { alikeAngular } from "@/public/fonts";

export default function DashboardBack() {
    return (
        <div className={`flex items-center justify-center min-h-screen w-full bg-[#020617] text-slate-200 selection:bg-blue-500/30 overflow-x-hidden ${alikeAngular.className}`}>
            <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(30,58,138,0.15),transparent)] pointer-events-none" />
            <div className="w-6/8 h-screen bg-black border-r-4 border-l-4 border-primary"/>
        </div>
    )
}