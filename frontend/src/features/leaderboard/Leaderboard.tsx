import { alikeAngular, crossaintOne } from "@/public/fonts";

export default function Leaderboard() {
  return (
    <div className={`w-full max-w-sm mx-auto rounded-xl border border-slate-800 bg-slate-950/90 p-3 shadow-2xl shadow-slate-950/50 backdrop-blur-xl mt-8 ${alikeAngular.className}`}>
      <h1 className={`text-xl font-bold mb-2 text-accent ${crossaintOne.className}`}>Leaderboard</h1>
      <p className="text-secondary mb-3 text-xs">Top players and their ranks.</p>

      <div className="space-y-2">
        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2">
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">Rank</span>
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">Player</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2">
          <span className="font-semibold text-sm text-accent">1</span>
          <span className="font-medium text-accent text-xs">Name_1</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2">
          <span className="font-semibold text-sm text-accent">2</span>
          <span className="font-medium text-accent text-xs">Name_2</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-lg border border-slate-800 bg-slate-900/80 p-2">
          <span className="font-semibold text-sm text-accent">3</span>
          <span className="font-medium text-accent text-xs">Name_3</span>
        </div>
      </div>
    </div>
  );
}
