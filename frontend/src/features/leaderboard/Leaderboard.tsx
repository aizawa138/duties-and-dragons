import { alikeAngular, crossaintOne } from "@/public/fonts";

export default function Leaderboard() {
  return (
    <div className={`w-full max-w-lg mx-auto rounded-2xl border border-slate-800 bg-slate-950/90 p-4 shadow-2xl shadow-slate-950/50 backdrop-blur-xl ${alikeAngular.className}`}>
      <h1 className={`text-2xl font-bold mb-3 text-accent ${crossaintOne.className}`}>Leaderboard</h1>
      <p className="text-secondary mb-4 text-sm">Top players and their ranks.</p>

      <div className="space-y-3">
        <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">Rank</span>
          <span className="text-xs uppercase tracking-[0.2em] text-secondary">Player</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
          <span className="font-semibold text-base text-accent">1</span>
          <span className="font-medium text-accent text-sm">Name_1</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
          <span className="font-semibold text-base text-accent">2</span>
          <span className="font-medium text-accent text-sm">Name_2</span>
        </div>

        <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
          <span className="font-semibold text-base text-accent">3</span>
          <span className="font-medium text-accent text-sm">Name_3</span>
        </div>
      </div>
    </div>
  );
}
